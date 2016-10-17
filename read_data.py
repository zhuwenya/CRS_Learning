# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cPickle as pickle
from scipy.sparse import csr_matrix
import numpy as np
import csv

data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/index2product.pkl"
f=open(data_path,'rb')
user_coffee_matrix=pickle.load(f)
M=user_coffee_matrix.todense()

item_set=user_coffee_matrix.values()

csvfile =file('/home/wenya/dialogue_system/code/recommendation/demo/data/item_set.csv', 'wb')
writer = csv.writer(csvfile)
for i in item_set:
    writer.writerow(i.encode('utf-8'))


import codecs  
  
with open('/home/wenya/dialogue_system/code/recommendation/demo/data/item_set.csv', 'w') as f:  
    for i in item_set:
        f.write(codecs.BOM_UTF8)  
        f.write('%s,1,3\n' % i.encode('utf-8')) 
        
import csv

csvfile = file('/home/wenya/dialogue_system/code/recommendation/demo/data/item_set.csv', 'rb')
reader = csv.reader(csvfile)
i=0
for line in reader:
    feature=line
    if i==2:
        break
    i+=1
feature=feature[]

with open('/home/wenya/dialogue_system/code/recommendation/demo/data/feature.txt', 'w') as f:  
    for i in feature:
        f.write(i) 
        f.write("\n")
        
feature_index=dict()
for i in range(len(feature)):
    feature_index[feature[i]]=i
    
data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/feature_index.pkl"
f=open(data_path,'r')
pickle.dump(feature_index,f)

feature_index=pickle.load(f)
index2feature=dict([(v, k) for k, v in feature_index.iteritems()])

data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/index2product.pkl"
f=open(data_path,'r')
index2product=pickle.load(f)

product2index=dict([(v.encode('utf8'), k) for k, v in index2product.iteritems()])
x=u'\ufeff\u62ff\u94c1'
y=u'\u62ff\u94c1'
print(x)
y='拿铁'
x==y

x
y
product2index[]

"拿铁".decode('utf-8')

data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/item_feature_matrix.pkl"
f=open(data_path,'r')
item_feature_matrix_raw=pickle.load(f)

import chardet
chardet.detect([u'\ufeff\u62ff\u94c1'])   
import csv


data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/feature_index.pkl"
f=open(data_path,'r')
feature_index=pickle.load(f)


def list2string(l):
    s=""
    for i in l:
        s=s+i
    return s
    
def strIntersection(s1, s2):
  out = ""
  for c in s1:
    if c in s2 and not c in out:
      out += c
  return out
  
  
x=strIntersection("太苦了", "酸甜苦")


data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/user_coffee_matrix_new.pkl"
f=open(data_path,'rb')
user_coffee_matrix=pickle.load(f)
(user_num,item_num)=user_coffee_matrix.shape
hidden_size=20
user_matrix=np.random.rand(user_num,hidden_size)
item_matrix=np.random.rand(item_num,hidden_size)
data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/user_embedding.pkl"
f=open(data_path,'r')
pickle.dump(user_matrix,f)
data_path="/home/wenya/dialogue_system/code/recommendation/demo/data/item_embedding.pkl"
f=open(data_path,'r')
pickle.dump(item_matrix,f)
