import pickle
import numpy as np
from collections import deque

def load_user_data(vdb, vq):
    '''
    load the user preference vector db from /profile
    '''
    # call this whenever we run the app
    with open('vdb.pkl', 'rb') as f:
        vdb = pickle.load(f)

    with open('vq.pkl', 'rb') as f:
        vq = pickle.load(f)
    
    return vdb, vq

def save_user_data_st(vq):
    '''
    save short-term 'staging' preferences
    '''

    with open('vq.pkl', 'wb') as f:
        pickle.dump(vq, f)
    
    return

def save_user_data_lt(vdb, vq):
    '''
    save long-term user preference vector db
    '''
    with open('vdb.pkl', 'wb') as f:
        pickle.dump(vdb, f)

    return

def reset_vdb(vdb):
    '''
    reset the user preference vector db to empty
    '''
    vdb = deque() # hold user preferences 300-d embedding vectors
    vdb.append(np.zeros((0,300), dtype=np.float32))

    save_user_data_lt(vdb)
    return

def reset_vq():
    '''
    reset the user staging queue
    '''
    vq = deque() # queue holding 300-d embedding vectors
    vq.append(np.zeros((0,300), dtype=np.float32))

    save_user_data_st(vq)
    return