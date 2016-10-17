# -*- coding: utf-8 -*-
# detect the useful information based on the user's response given the system action
# the useful information includes:
# 1) the preference on the product
# 2) the preference on the feature
import numpy as np
import utils
from utils import *

root="/home/ubuntu/Collect_Data/CRS_Learning/data/"
data_path="/home/ubuntu/Collect_Data/CRS_Learning/data/feature_index.pkl"
f=open(data_path,'r')
feature2index=pickle.load(f)
f.close()

class UserDetection(object):
    def __init__(self):
        self.product_list=self.get_key_words("product.txt"); #contain the name of the product
        self.feature_list=self.get_key_words("feature.txt"); #contain the name of the feature
        self.feature="苦甜酸"
        self.like_feature_list=self.get_key_words("like_feature.txt")
        self.dislike_feature_list=self.get_key_words("dislike_feature.txt")
        #self.nocare_feature_list=self.get_key_words("nocare_feature.txt")
        self.like_product_list=self.get_key_words("like_product.txt")
        self.dislike_product_list=self.get_key_words("dislike_product.txt")


    def get_feedback(self,user_say,action,product,feature):
        """
        user_say: the user's current utterance
        (when the user rejects the product recommendation, they may indicate what the feature they doesn't like)
        (when the agent inquires the preference on the feature, the user will reply their preference)
        action, product and feature describe the sentence of the system
        """
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
            for preference in self.like_product_list:
                preference=preference.decode('utf-8')
                try:
                    prefer_product_set.append(user_say.index(preference))
                except ValueError:
                    pass
            for preference in self.dislike_product_list:
                preference=preference.decode('utf-8')
                try:
                    no_prefer_product_set.append(user_say.index(preference))
                except ValueError:
                    pass
            for feature in self.feature_list:
                feature=feature.decode('utf-8')
                try:
                    feature_set.append(user_say.index(feature))
                except ValueError:
                    pass

            for preference in self.dislike_feature_list:
                preference=preference.decode('utf-8')
                try:
                    no_prefer_feature_set.append(user_say.index(preference))
                except ValueError:
                    pass
            if len(prefer_product_set)!=0 and len(no_prefer_product_set)==0:
                user_prefer_product="like"
            if len(no_prefer_product_set)!=0 and len(feature_set)==0:
                user_prefer_product="dislike"
            if len(feature_set)!=0:
                user_feature.append(feature_set[0])
                if len(no_prefer_feature_set)!=0:
                    user_pre_feature="dislike"
                else:
                    user_pre_feature="like"
            if len(feature_set)==0 and len(prefer_product_set)==0 and len(no_prefer_product_set)==0:
                pass
        if action=="feature":
            user_feature.append(feature)
            for preference in self.dislike_feature_list:
                preference=preference.decode('utf-8')
                try:
                    no_prefer_feature_set.append(user_say.index(preference))
                except ValueError:
                    pass
            if len(no_prefer_feature_set)!=0:
                user_pre_feature="dislike"
            else:
                user_pre_feature="like"
        return user_feature,user_pre_feature,user_product,user_prefer_product

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
