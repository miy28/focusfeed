import pickle
import gensim
import re
import numpy as np
from difflib import get_close_matches
from gensim.models import Word2Vec, FastText
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import cosine

from data_models import load_user_data, save_user_data_st, save_user_data_lt, reset_vdb, reset_vq

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

def commit_staging(vdb, vq): # once queue reached max size, dump into vdb
    '''
    batch-storing user interactions for cleaner processing. allow for more features to be added in the future.
    '''

    while vq:
        vec = vq.popleft()
        vdb.append(vec)

    while len(vdb) > 1000:
        vdb.popleft()

    return vdb, vq

def recluster(vdb):
    '''
    - adjust clusters based on queued vectors and get new centroids
    - basically recompute ('refresh') user preferences
    '''

    # prioritize clusters with most number of points
    # check if dbscan eps gives meaningful clusters 
    # if its just a cluster of single point, fallback to word2vec.get_nearest -> adjacents

    queries = []
    adjacents = []
    curious = []
    # apply negative vectors *after* finding each of these^

    model = DBSCAN(eps=0.3, min_samples=5, metric='cosine').fit(vdb)

    labels = model.labels_

    if set(labels) == {-1}: # vdb too sparse for clustering. get closest two vectors and expand from there
        nearest = get_nn(vdb)
        queries.append(nearest)
        return queries

    # 

    return queries, adjacents, curious

def flush_vdb(vdb): # unused
    '''
    prune oldest vectors in the vdb
    '''

    save_user_data_lt(vdb)
    return

def get_nn(vdb):
    # find closest two vectors in the vdb based on cosine similarity, as a starting point
    if len(vdb) < 2:
        return None, None  # Not enough vectors to compare

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

    w2v_similar = model_w2v.wv.similar_by_vector(centroid, topn=8)
    for vec in w2v_similar:
        nearest.append(model_w2v.wv[vec])

    return nearest

def fetch_articles_with_bias(queries, adjacents, curious, fresh, epsilon):
    N = 10 # number of total articles to fetch
    # fetch N=10 articles total
    # queries: list of exact newsAPI keywords (primary user interests)
    # adjacents: list of closely related keywords, may not be exact newsAPI keywords
    # curious: list of loosely related keywords, may not be exact newsAPI keywords
    # explore = epsilon * N articles pulled from outlier clusters
    # fresh * (N - explore) articles pulled from KNN of each top 5 keyword

    articles = []

    return articles