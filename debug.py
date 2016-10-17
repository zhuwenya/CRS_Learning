# -*- coding: UTF-8 -*-
from __future__ import print_function
import sys
import jieba as jieba_rnn
import cPickle as pickle
from scipy.sparse import csr_matrix
import numpy as np
import csv
from system_response import *
from user_detector import *
import utils
data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/index2product.pkl"
f=open(data_path,'r')
index2product=pickle.load(f)
product2index=dict([(v, k) for k, v in index2product.iteritems()])

jieba = jieba_rnn.Tokenizer()
jieba.load_userdict("/home/wenya/dialogue_system/code/recommendation/demo/data/dict.txt.coffe")



#random generate the user embedding and item embedding
data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/user_coffee_matrix_new.pkl"
f=open(data_path,'rb')
user_coffee_matrix=pickle.load(f)
(user_num,item_num)=user_coffee_matrix.shape
hidden_size=20
user_matrix=np.random.rand(user_num,hidden_size)
item_matrix=np.random.rand(item_num,hidden_size)


user_embedding=np.mean(user_matrix,axis=0)
Agent=SystemResponse()
User=UserDetection()

"""
sentence,action,recommend_product,inquiry_feature=Agent.generate_sys_response(user_embedding,item_matrix)
print("System:"+sentence)
sent_user = raw_input("user: ")
sent_user=[i for i in jieba.cut(sent_user)]
print(sent_user)
user_feature,user_pre_feature,user_product,user_prefer_product=User.get_feedback(sent_user,action,recommend_product,inquiry_feature)
print(user_feature)
print("user_pre_feature"+user_pre_feature)
print(user_product)
print("user_prefer_product"+user_prefer_product)
"""
