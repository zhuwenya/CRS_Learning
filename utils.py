# -*- coding: UTF-8 -*-
import jieba
import math
import numpy as np
import pickle

data_path="/home/ubuntu/collect_data/CRS_Learning/data/item_feature_matrix.pkl"
f=open(data_path,'r')
item_feature_matrix=pickle.load(f)
f.close()

data_path="/home/ubuntu/collect_data/CRS_Learning/data/feature_index.pkl"
f=open(data_path,'r')
feature_index=pickle.load(f)
f.close()

data_path="/home/ubuntu/collect_data/CRS_Learning/data/user_coffee_matrix_new.pkl"
f=open(data_path,'r')
user_coffee_matrix=pickle.load(f)
f.close()
(user_num,item_num)=user_coffee_matrix.shape

data_path="/home/ubuntu/collect_data/CRS_Learning/data/user_embedding.pkl"
f=open(data_path,'r')
User_Embedding=pickle.load(f)
f.close()
(_,hidden_size)=User_Embedding.shape
data_path="/home/ubuntu/collect_data/CRS_Learning/data/item_embedding.pkl"
f=open(data_path,'r')
Item_Embedding=pickle.load(f)
f.close()


def sigmoid(x):
    return (1 / (1 + math.exp(-0.4*x)))



def product_match_feature(feature):
    """
    return the products which match the feature
    """
    feature=feature[0]
    product=(np.where(item_feature_matrix[:,feature]>=1))[0]
    product=product.tolist()
    return product

def update_user_embedding(user_feature,user_pre_feature,user_product,user_prefer_product):
    """
    update the user's latent embedding
    """
    weights=np.ones((user_num,1))
    if user_prefer_product=="dislike" and len(user_product)!=0:
        product_index=user_product[0]
        user_group=np.where(user_coffee_matrix[:,product_index]>=1)
        if len(user_group)!=0:
            for i in user_group:
                weights[i,0]=0.3
    if user_prefer_product=="like" and len(user_feature)!=0:
        feature_index=user_feature[0]
        products=product_match_feature(feature_index)
        if len(products)!=0:
            for product in products:
                user_group=np.where(user_coffee_matrix[:,product_index]>=1)
                if len(user_group)!=0:
                    for i in user_group:
                        weights[i,0]=1.5
    if user_prefer_product=="dislike" and len(user_feature)!=0:
        feature_index=user_feature[0]
        products=product_match_feature(feature_index)
        if len(products)!=0:
            for product in products:
                user_group=np.where(user_coffee_matrix[:,product_index]>=1)
                if len(user_group)!=0:
                    for i in user_group:
                        weights[i,0]=0.5
    W=np.repeat(weights,hidden_size,axis=1)
    User_embedding=User_Embedding*W
    user_embedding=np.mean(User_embedding,axis=0)/np.sum(weights)
    return user_embedding

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
