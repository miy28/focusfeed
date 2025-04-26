import os
import pickle
import numpy as np
from collections import deque

from core.data_models import ArticleIterator, FeedNote
from api.nytimes_api import fetch_nytimes_articles

MAX_WINDOW_LEN = 1000
VDB_PATH = '/profile/vdb.pkl'
KDB_PATH = '/profile/kdb.pkl'
VQ_PATH = '/profile/vq.pkl'
MOOD_PATH = '/profile/mood.pkl'

def init_user_data():
    if os.path.exists(VDB_PATH) and os.path.exists(VQ_PATH) and os.path.exists(MOOD_PATH):
        return
    
    # 'browsing history', our vector database. holding user preferences 300-d embedding vectors
    vdb = deque(maxlen=MAX_WINDOW_LEN)
    # vdb.append(np.zeros((0,300), dtype=np.float32))
    kdb = deque(maxlen=MAX_WINDOW_LEN) # mapping to original keywords for reverse-lookup
    
    # staging queue, holding 300-d embedding vectors
    vq = deque()

    save_pkl(VDB_PATH, vdb)
    save_pkl(KDB_PATH, kdb)
    save_pkl(VQ_PATH, vq)

    # true 'user preferences' model. how the user is currently feeling, as per the last recluster.
    #     queries: list of exact newsAPI keywords (primary user interests)
    #     adjacents: list of closely related keywords, may not be exact newsAPI keywords
    #     curious: list of loosely related keywords, may not be exact newsAPI keywords
    mood = [[], [], []] # queries[], adjacents[], curious[]
    save_pkl(MOOD_PATH, mood)

def get_pkl(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def save_pkl(path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def get_user_data(vdb, vq):
    '''
    load the user preference vector db from /profile
    '''
    # call this whenever we run the app
    with open('vdb.pkl', 'rb') as f:
        vdb = pickle.load(f)

    with open('vq.pkl', 'rb') as f:
        vq = pickle.load(f)
    
    return vdb, vq

def reset_user_data(vdb, vq):
    '''
    reset user preference vector db to empty
    '''
    vdb = deque()
    kdb = deque()
    vq = deque()
    mood = [[], [], []] # no mood. numb

    save_pkl(VDB_PATH, vdb)
    save_pkl(KDB_PATH, kdb)
    save_pkl(VQ_PATH, vq)
    save_pkl(MOOD_PATH, mood)

