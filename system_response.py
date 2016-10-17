# -*- coding: utf-8 -*-
# system generate the response given the action and corresponding value
# p(s/action,value)
#self.action: 0(recommend product) or 1 (ask for the preference on the product feature)
import numpy as np
import utils
from utils import *
import cPickle as pickle
action_name={0:"product",1:"feature"}
action_index=dict([(v, k) for k, v in action_name.iteritems()])
data_path="/home/ubuntu/Collect_Data/CRS_Learning/data/index2product.pkl"
f=open(data_path,'r')
index2product=pickle.load(f)
product2index=dict([(v, k) for k, v in index2product.iteritems()])

data_path="/home/ubuntu/Collect_Data/CRS_Learning/data/feature_index.pkl"
f=open(data_path,'r')
feature2index=pickle.load(f)
index2feature=dict([(v, k) for k, v in feature2index.iteritems()])


root="/home/ubuntu/collect_data/CRS_Learning/data/"
class SystemResponse(object):
    def __init__(self):
        self.action="product" # the action of the current step
        self.action_prob=[1,0] #the probability of the two action; default to recommend the product to the user
        self.Action_Set=[]#the list to contain the paste actions
        self.product=[i for i in xrange(60)] # contain name of all product
        self.feature=[i for i in xrange(21)] #contain the feature of the product
        self.relax_feature=False
        self.tignthen_feature=False
        self.new_product=self.get_key_words('new_product.txt')# contain the name of the new product
        self.hot_product=self.get_key_words('hot_product.txt')


    def intention_detection(self):
        """
        use thif module to compute the probability fo the two action
        """
        if len(self.Action_Set)==0:
            self.action_prob=[1,0]
        else:
            self.action_prob=[sum(self.Action_Set)/float(len(self.Action_Set)),1-sum(self.Action_Set)/float(len(self.Action_Set))]
        action=action_name[np.argmax(self.action_prob)] # return the "product" or "feature"

        """
        check the whether the action is legal(like whether all the feature has been asked)
        """
        if action=="feature":
            if len(self.feature)==0:
                action=="product"
        return action

    def get_product(self,user_embedding,item_embedding):
        """
        We have enetred the recommending product module
        Now we need to compute what product to recommend
        input:
        user_embedding -- the user latent vector of the current user
        item_embedding -- the item latent matrix
        """
        if self.action !="product":
            raise ValueError('not in the recommending product action')

        """
        compute the score of the products based on the learnt user embedding and item embedding
        """
        recommend_product=[]
        if len(self.product)==0:
            # we donot have the products to match the feature conditions of the user
            # we need relax the feature
            Recommend_Product=[]
            self.relax_feature=True
        product_score=np.dot(item_embedding,user_embedding)
        product_belief=np.array([sigmoid(x) for x in product_score])
        product_recommend=(np.where(product_belief>0.5))[0] # the sorted prodcut of the product(ascending order)
        recommend_product=np.intersect1d(np.array(self.product),product_recommend)

        np.random.shuffle(recommend_product)
        if len(recommend_product)==0:
            self.tignthen_feature=True
            Recommend_Product=[]
        else:
            Recommend_Product=[recommend_product[0]]
            self.product.remove(recommend_product[0])
        return Recommend_Product

    def get_feature(self):
        """
        we have entered the inquring module to obtain the user's preference on the products
        now we adopt the random picking policy
        """
        np.random.shuffle(self.feature)
        inquiry_feature=self.feature[0]
        self.feature.remove(inquiry_feature)
        return inquiry_feature

    def get_key_words(self,file_name):
         key_words = list();
         print (root+file_name);
         try:
            with open(root+file_name) as file:
                for line in file:
                   key_words.append(line.strip());
         except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror);

         return key_words

    def update_product(self,product,dislike):
         """
         we need to update the product by filtering the products which have been recommended
         (if dislike,we should remove it from self.product)
         """
         if dislike=="dislike":
             for i in product:
                 try:
                     self.product.remove(i)
                 except ValueError:
                     pass
         return -1


    def update_feature(self,feature,dislike):
        """
        (if informing some feature that the user dislikes, then we filter some product which matches to this feature)
        (if informing some feature that the user likes,then we should just include products which matches the feature)
        """
        flag=0
        if dislike=="dislike":
            products=product_match_feature(feature)
            if len(products)!=0:
                product=[i for i in self.product if i not in products]
        else:
            product=product_match_feature(feature)
        if len(product)==0:
            flag=1
        self.product=product
        return flag


    def generate_sys_response(self,user_embedding,item_embedding):
        """
        generate the sentence of the system based on the current action
        """
        recommend_product=[]
        inquiry_feature=[]
        # get the current action
        action=self.intention_detection()
        if action=="product":
            recommend_product=self.get_product(user_embedding,item_embedding)
            if len(recommend_product)!=0:
                sentence=self.sys_utter(action,recommend_product[0],[])
                self.Action_Set.append(action_index[action])
            else:
                if self.relax_feature==True:
                    sentence="不好意思，你要的饮品本店暂时没有"
                if self.tignthen_feature==True:
                    action="feature"
        if action=="feature":
            inquiry_feature=self.get_feature()
            self.Action_Set.append(action_index[action])
            sentence=self.sys_utter(action,[],inquiry_feature)
        return sentence,action,recommend_product,inquiry_feature


    def sys_utter(self,action,product,feature):
        """
        system speaking based on the action and the value
        """
        if action=="product":
            product=index2product[product].encode('utf-8')
            if product in self.new_product:
                sentence=product+"是本店新推出的产品，想要尝试一下么？"
            elif product in self.hot_product:
                sentence=product+"是本店的热销产品奥"
            else:
                sentence=self.sys_utter_template(product)
        if action=="feature":
            feature_name=index2feature[feature]
            if feature>=18:
                templates=["喜欢"+feature_name+"的么？",feature_name+"一点？"]
            else:
                templates=["要加"+feature_name+"么？","有"+feature_name+",可以么？","喜欢"+feature_name+"吗？"]
            np.random.shuffle(templates)
            sentence=templates[0]
        return sentence

    def get_product_index(self):
        product_index=[]
        for i in self.product:
            index=product2index[i.decode('utf-8')]
            product_index.append(index)
        return product_index

    def get_index_product(self,product):
        product=product.decode('utf-8')
        return -1

    def sys_utter_template(self,product):
        if len(self.Action_Set)!=0 and self.Action_Set[-1]==action_index["feature"]:
            templates=[product+"?","要不要"+product+"?",product+"满足你的要","好的，"+product+" 可能是您想要的","好的,向您推荐"+product]
            np.random.shuffle(templates)
        else:
            templates=[product+"?","要不要"+product+"?",product+"很不错呢","好的，"+product+"可能是您想要的","好的,向您推荐"+product]
            np.random.shuffle(templates)
        return templates[0]
