# -*- coding: UTF-8 -*-
from __future__ import print_function
import jieba as jieba_rnn
from collections import deque
from system_response import *
from user_detector import *
import cPickle as pickle
from utils import *
data_path="/home/ubuntu/Collect_Data/CRS_Learning/data/"



def cut_sentence(string):
    sent = ' '.join(jieba.cut(string)).encode('utf-8')
    sent_split=[i.encode('utf-8') for i in jieba.cut(string)]
    return sent,sent_split

class recommend_agent(object):
    def __init__(self):
        print("系统初始化.....")
        jieba = jieba_rnn.Tokenizer()
        jieba.load_userdict("/home/ubuntu/Collect_Data/CRS_Learning/data/dict.txt.coffe")
        print("载入数据")

        User_Embedding=pickle.load(open(data_path+"user_embedding.pkl"))
        Item_Embedding=pickle.load(open(data_path+"item_embedding.pkl"))
        self.Item_Embedding=np.transpose(Item_Embedding)
        print("初始化用户兴趣向量")
        self.user_embedding=np.mean(User_Embedding,axis=0)
        self.Agent=SystemResponse()
        self.User=UserDetection()
        print("初始化完毕")
        print("欢迎来到对话推荐系统,CRS向您推荐咖啡等其他饮品")
        print("友情提示：如果您想离开此系统，请输入q")
        print()
        print("当前进入drink推荐系统")
        print("开始体验对话推荐")
        self.agent_response="请问有什么想喝的？"
        self.num=0



    def get_first_response(self):       
        sent_agent,action,recommend_product,inquiry_feature=self.Agent.generate_sys_response(self.user_embedding,self.Item_Embedding)
        self.agent_response=sent_agent
        self.action=action
        self.recommend_product=recommend_product
        self.inquiry_feature=inquiry_feature
        return self.agent_response,self.action,self.recommend_product,self.inquiry_feature

    def get_response(self,in_msg):
        sent_user = in_msg
        sent_user=[i for i in jieba.cut(sent_user)]
        if sent_user == "q":
            self.agent_response="欢迎再次光临。祝您开心每一天！"
            return self.agent_response,None,None,None
        else:
            user_feature,user_pre_feature,user_product,user_prefer_product=self.User.get_feedback(sent_user,self.action,self.recommend_product,self.inquiry_feature)
            if len(user_product)!=0 and user_prefer_product=="like":
                self.agent_response="好的。欢迎再次光临。祝您开心每一天！"
                return self.agent_response,None,None,None
            else:
                if len(user_feature)==0 and len(user_pre_feature)==0 and len(user_product)==0 and len(user_prefer_product)==0:
                    self.agent_response,self.action,self.recommend_product,self.inquiry_feature=self.Agent.generate_sys_response(self.user_embedding,self.Item_Embedding)
                    return self.agent_response,self.action,self.recommend_product,self.inquiry_feature
                if len(user_feature)!=0:
                    flag=self.Agent.update_feature(user_feature,user_pre_feature)
                    if flag==1:
                        self.agent_response="抱歉,实在找不到你要的饮品！"
                        return self.agent_response,None,None,None
                if len(user_product)!=0 and user_prefer_product=="dislike":
                    self.Agent.update_product(user_product,user_prefer_product)
                self.user_embedding=update_user_embedding(user_feature,user_pre_feature,user_product,user_prefer_product)
                self.agent_response,self.action,self.recommend_product,self.inquiry_feature=self.Agent.generate_sys_response(self.user_embedding,self.Item_Embedding)
                return self.agent_response,self.action,self.recommend_product,self.inquiry_feature
