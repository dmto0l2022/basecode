import pickle

from flask import request, session

import requests
import json
import redis

default_dmtool_userid = '0'

class GetUserID():
    def __init__(self):
        self.dmtool_userid = '0'
        self.redisserver = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
        self.Try2GetUser()
    def Try2GetUser(self):
        #try:
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        session_key = request.cookies.get('session')
        #print('list all keys : session key >>',session_key)
        redis_session_key = "session:"+session_key
    
        session_data = self.redisserver.get(redis_session_key)
        print('--------- get dmtool user function -- decoded val------------------------------')
        #decoded_val = pickle.loads(session_data)
        #print(decoded_val)
        
        self.dmtool_userid = decoded_val['dmtool_userid']
        print('gdu : dmtool_userid >>>>>>>>>>>>' , self.dmtool_userid)
        #except:
        #    print('No session >>>>>')
        #    self.dmtool_userid = '0'
