import tensorflow as tf
import cPickle as pickle
from scipy.sparse import csr_matrix
import numpy as np

data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/user_coffee_matrix.pkl"

f=open(data_path,'rb')
user_coffee_matrix,column_to_pinyin, userid_to_row =pickle.load(f)
M=user_coffee_matrix.todense()

class Config (object):
    User_Item_Matrix=M
    rank=10 # the length of the hidden vector
    lr=0.1 # the learning rate
    max_iter=10000
    .min_delta=0.001
