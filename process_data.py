# -*- coding: UTF-8 -*-
from __future__ import print_function
import sys
import jieba as jieba_rnn
import cPickle as pickle
from scipy.sparse import csr_matrix
import numpy as np
import csv


data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/feature_index.pkl"
f=open(data_path,'r')
feature_index=pickle.load(f)
data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/index2product.pkl"
f=open(data_path,'r')
index2product=pickle.load(f)
product2index=dict([(v, k) for k, v in index2product.iteritems()])
item_feature_matrix=np.zeros((len(product2index),len(feature_index)))

f=open('/home/wenya/dialogue_system/code/recommendation/demo/data/item_set.csv', 'r')
i=0
while 1:
    line = f.readline()
    if not line:
        break
    if i==0:
        pass
    else:
        line=line.strip('\n')
        line=line.split(",")
        product=line[0].decode('utf-8')
        print(product)
        if product[0]== u'\ufeff':
            product=product[1:]
        raw=product2index[product]
        colunm=line[1:]
        item_feature_matrix[raw,:]=colunm
        print (colunm)
    i+=1


data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/item_feature_matrix.pkl"
f=open(data_path,'w')
pickle.dump(item_feature_matrix,f)



"""
data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/user_coffee_matrix.pkl"
f=open(data_path,'rb')
user_coffee_matrix,column_to_pinyin, userid_to_row =pickle.load(f)
M=user_coffee_matrix.todense()
(User_num,Item_num)=M.shape
pinyin_to_column=dict([(v, k) for k, v in column_to_pinyin.iteritems()])

root="/home/wenya/dialogue_system/code/recommendation/demo/data/"

data_path=root+"product_name.txt"

product_dict=dict()
product=[]
file = open(data_path)
while 1:
    line = file.readline()
    if not line:
        break
    line=line.strip("\n")
    x=line.split("|")
    key=x[0].decode('utf-8')
    value=x[1:]
    product_dict[key]=value
    product.append(x[0].decode('utf-8'))


# find the user_item_vector for each item
User_Item_M=np.zeros((User_num,len(product)))
product_index=dict()
j=0
for item in product:
    name_set=product_dict[item]
    name_index=[pinyin_to_column[i] for i in name_set]
    item_vector=np.zeros((User_num,1))
    for i in name_index:
        item_vector+=M[:,i]
    User_Item_M[:,j]=item_vector.reshape((User_num))
    product_index[j]=item
    j+=1

data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/user_coffee_matrix_new.pkl"
f=open(data_path,'wb')
pickle.dump(User_Item_M,f)


data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/index2product.pkl"
f=open(data_path,'wb')
pickle.dump(product_index,f)
"""
