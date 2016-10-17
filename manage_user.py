import numpy as np
import time
from backend import *



class Manage_User(object):
    def __init__(self):
        self.user_instance=dict()
        self.user_time=dict()
        self.time_clean=60

    def add_user(self,user_id):
        # add new user
        if self.user_instance.has_key(key):
            self.user_instance[user_id]=recommend_agent()
        else:
            pass
    return None

    def obtain_user_instance(self,user_id,time):
         # obtain user's instance based on user's id
         self.add_user() # add new user(invalid for exsiting user)
         #when obtain this user's id, it means that this user is active
         self.user_time[user_id]=time
         return self.user_instance[user_id] #obtain the instance of the user based on user's id

    def clean_user(self):
        current_time= int(time.time())
        user_active=[k for k, v in self.user_time.iteritems() if v-current_time>0]
        clean_user_instance=dict((v, k) for k, v in self.user_instance.iteritems() if k in user_active)
        self.user_instance=clean_user_instance
        return None
