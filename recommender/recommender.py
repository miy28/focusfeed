import pickle
import gensim
import re
import random
import numpy as np
from difflib import get_close_matches
from gensim.models import Word2Vec, FastText
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import cosine

from core.data_models import fetch_articles, lookup_articles
from data_models import get_pkl, save_pkl, VDB_PATH, KDB_PATH, VQ_PATH, MOOD_PATH, MAX_WINDOW_LEN

model_w2v = Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True, norm_only=True)
model_ft = FastText.load_facebook_model('wiki.simple.bin')

'''
APPROACH #1 - get new articles
for each article:
split keywords (ex. "Tortoise (Music Group)") into individual words ("Tortoise", "Music", "Group"),
get embeddings via word2vec and compute vector average (centroid vector)
use new vec to get KNN to formulate new query word to fetch new articles (store UNIQUE into db)
'''

'''
APPROACH #2 - search existing articles (optimize space)
compile exhaustive vocab list of both:
(1) word2vec pretrained vocab
(2) article db keywords
store both on disk to compare
use difflib.get_close_matches() to get article db keywords that can be directly index on
'''

# word2vec.similar_by_vector() and word2vec.find_similar()

def init_preferences(topics):
    '''
    initialize recommender with list of user-provided topics
    also generate the first round of the feed!
    '''

    # when we start off.. let's immediately populate their preferences with articles based on their queries
    vdb = get_pkl(VDB_PATH) 

    for topic in topics:
        if len(vdb) > MAX_WINDOW_LEN: # enforce sliding window-based memory decay
            break
        articles_ait = fetch_articles(topic) # new articles
        for ait in articles_ait:
            for keyword in ait.keywords:
                vec = get_embedding(keyword)
                vdb.append(vec)
    
    save_pkl(VDB_PATH, vdb)

def get_embedding(keyword, cutoff=0.8):
    '''
    generate embeddings
    if needs parsing use difflib to get closest fuzzy match
    '''

    model_w2v_vocab = model_w2v.wv.keys()

    vec = model_w2v.wv[keyword]

    if keyword not in model_w2v_vocab: # handling out-of-vocabulary words
        close_matches = get_close_matches(keyword, model_w2v_vocab, n=3, cutoff=cutoff) # first fallback
        if close_matches:
            keyword = close_matches[0]
        else: # second fallback. if this fails just screw it man.
            delim = ",|;|\s|(|)" # common nytimesApi keyword punctuation
            sub_keywords = re.split(delim, keyword)
            vecs = [model_w2v.wv[k] for k in sub_keywords if k in model_w2v_vocab]
            if vecs:
                vec = np.mean(vecs, axis=0)
    
    return vec

def get_keyword(vec):
    # load vdb and kdb
    vdb = get_pkl(VDB_PATH)
    kdb = get_pkl(KDB_PATH)

    if vec in vdb: # first try vdb
        keyword = kdb[vdb.index(vec)]
    else: # otherwise use model gen
        keyword = model_w2v.wv.similar_by_vector(vec, topn=1)
    
    return keyword

def commit_staging(vdb, vq): # once queue reached max size, dump into vdb
    '''
    batch-storing user interactions for cleaner processing. allow for more functionality to be added in the future.
    '''

    while vq: # empty the staging queue
        vec, keyword = vq.popleft()
        vdb.append(vec)
        kdb.append(keyword)

    while len(vdb) > 1000: # enforce sliding window memory dropout
        vdb.popleft()

    save_pkl(VDB_PATH, vdb)
    save_pkl(KDB_PATH, vdb)
    save_pkl(VQ_PATH, vq)

    return vdb, vq

def recluster(vdb):
    '''
    - adjust clusters based on queued vectors and get new centroids
    - basically recompute or refresh user preferences
    '''

    # prioritize clusters with most number of points
    # check if dbscan eps gives meaningful clusters 
    # if its just a cluster of single point, fallback to word2vec.get_nearest -> adjacents

    # every time we recluster, we fetch new articles

    queries = [] # primary vecs
    adjacents = [] # border vecs
    curious = [] # noise vecs
    # apply negative vectors *after* finding each of these^

    model = DBSCAN(eps=0.3, min_samples=5, metric='cosine').fit(vdb) # perform density-aware clustering algorithm

    labels = model.labels_ # get results

    if set(labels) == {-1}: # vdb too sparse for clustering. get closest two vectors and expand from there
        nearest = get_nn(vdb) # use fallback method
        queries.extend(nearest)
        adjacents.extend(nearest)
        return queries



    mood = [queries, adjacents, curious] # update user preferences
    save_pkl(MOOD_PATH, mood)

    return queries, adjacents, curious

def flush_vdb(vdb): # unused
    '''
    prune oldest vectors in the vdb
    '''
    # save_user_data_lt(vdb)
    return

def get_nn(vdb):
    '''
    to be used for an edge case, when our vdb is too sparse to meaningfully cluster
    finds closest two vectors in the vdb based on cosine similarity, as a starting point
    '''
    if len(vdb) < 2: 
        return None, None # okay. we really can't do anything here. 93

    nearest = []
    min_distance = float('inf')
    closest_pair = (None, None)

    for i in range(len(vdb)):
        for j in range(i + 1, len(vdb)):
            dist = cosine(vdb[i], vdb[j])
            if dist < min_distance:
                min_distance = dist
                closest_pair = (vdb[i], vdb[j])

    nearest.append(closest_pair[0])
    nearest.append(closest_pair[1])

    centroid = np.mean([closest_pair[0], closest_pair[1]])

    w2v_similar = model_w2v.wv.similar_by_vector(centroid, topn=8) # fulcrum. COME IN
    for vec in w2v_similar:
        nearest.append(model_w2v.wv[vec])

    return nearest

def get_articles_with_bias(mood, epsilon=0.3, fresh=0.0, N=10):
    # epsilon: fraction of articles that are 'exploratory'
    # fresh: fraction of articles to fetch. applied after epsilon
    # 'adjacent' is always gonna be 50% of non-exploratory portion

    queries, adjacents, curious = mood
    articles = []

    num_primary = (1 - epsilon) * N
    num_explore = epsilon * N

    N_ps = num_primary * (1 - fresh) # num_primary_stale
    N_pf = num_primary * fresh
    N_es = num_explore * (1 - fresh)
    N_ef = num_explore * fresh
    
    # stale -> sql lookup; fresh -> nytimesAPI
    primary_stale_vecs = random.sample(queries, int(N_ps // 2)) # balance queries and adjacent evenly
    primary_fresh_vecs = random.sample(queries, int(N_pf // 2))
    adjacent_stale_vecs = random.sample(adjacents, int(N_ps // 2))
    adjacent_fresh_vecs = random.sample(adjacents, int(N_pf // 2))
    explore_stale_vecs = random.sample(curious, int(N_es)) if len(curious) >= int(N_es) else curious
    explore_fresh_vecs = random.sample(curious, int(N_ef)) if len(curious) >= int(N_ef) else curious

    for i in range(0, len(primary_stale_vecs), 2):
        if (i + 1) < len(primary_stale_vecs): # ensure pairs exist
            vec1 = primary_stale_vecs[i]
            vec2 = primary_stale_vecs[i + 1]
            keyword1 = get_keyword(vec1)
            keyword2 = get_keyword(vec2)
            a = lookup_articles(keyword1, keyword2)
            if a:
                articles.extend(a)
            else: # not enough articles in sql db, lets get double the amount of articles
                a1 = fetch_articles(keyword1) # 10 articles
                a2 = fetch_articles(keyword2) # 10 more
                articles.extend(a1)
                articles.extend(a2)
    

    return articles[:N] # discretized if need be