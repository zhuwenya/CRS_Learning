# -*- coding: UTF-8 -*-
import numpy as np
import utils
from utils import *
import jieba as jieba_rnn

jieba = jieba_rnn.Tokenizer()
jieba.load_userdict("/home/wenya/dialogue_system/code/recommendation/demo/data/dict.txt.coffe")

def get_key_words(self, file_name):
 key_words = list();
 print root+file_name;
 try:
    with open(root+file_name) as file:
        for line in file:
           key_words.append(line.strip());
 except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror);

 return key_words;

root="/home/wenya/dialogue_system/code/recommendation/demo/data/"

product_list=get_key_words("product.txt")
feature_list=get_key_words("feature.txt"); #contain the name of the feature
like_feature_list=get_key_words("like_feature.txt")
dislike_feature_list=get_key_words("dislike_feature.txt")
#nocare_feature_list=get_key_words("nocare_feature.txt")
like_product_list=get_key_words("like_product.txt")
dislike_product_list=get_key_words("dislike_product.txt")

user_say="好的"
user_say=[i for i in jieba.cut(user_say)]
action="product"
product=11
feature=[]

user_feature=[]
user_pre_feature=""
user_product=[]
user_prefer_product=""
prefer_product_set=[]
no_prefer_product_set=[]
feature_set=[]
no_prefer_feature_set=[]
if action=="product":
    user_product=product
    for preference in like_product_list:
        preference=preference.decode('utf-8')
        try:
            prefer_product_set.append(user_say.index(preference))
        except ValueError:
            pass
    for preference in dislike_product_list:
        preference=preference.decode('utf-8')
        try:
            no_prefer_product_set.append(user_say.index(preference))
        except ValueError:
            pass
    for feature in feature_list:
        feature=feature.decode('utf-8')
        try:
            feature_set.append(user_say.index(preference))
        except ValueError:
            pass
    for preference in dislike_feature_list:
        preference=preference.decode('utf-8')
        try:
            no_prefer_feature_set.append(user_say.index(preference))
        except ValueError:
            pass
    if len(prefer_product_set)!=0 and len(no_prefer_product_set)==0:
        user_prefer_product="like"
        return user_prefer_product
    if len(no_prefer_product_set)!=0 and len(feature_set)==0:
        user_prefer_product="dislike"
        return user_prefer_product
    if len(feature_set)!=0:
        user_feature=feature_Set[0]
        if len(no_prefer_feature_set)!=0:
            user_pre_feature="dislike"
        else:
            user_pre_feature="like"
    if len(feature_set)==0 and len(prefer_product_set)==0 and len(no_prefer_product_set)==0:
        pass
if action=="feature":
    user_feature=feature
    for preference in dislike_feature_list:
        preference=preference.decode('utf-8')
        try:
            no_prefer_feature_set.append(user_say.index(preference))
        except ValueError:
            pass
    if len(no_prefer_feature_set)!=0:
        user_pre_feature="dislike"
    else:
        user_pre_feature="like"
