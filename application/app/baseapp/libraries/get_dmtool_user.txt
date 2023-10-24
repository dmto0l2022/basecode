import redis
import pickle
from flask import request

r = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
session_key = request.cookies.get(self.SESSION_COOKIE_NAME)
print('session key >>',session_key)
redis_session_key = 'session:'+session_key
print('redis_session_key >>',redis_session_key)
#all_keys = r.keys('*')
#print("redis all keys >>>>>", all_keys)
#print("redis all keys >>>>>", type(all_keys))
#print("redis get session data")
'''
for k in all_keys:
    val = r.get(k)
    print("k>>>>" , k)
    print('---------------------------------------')
    print("val>>>>", val)
    print('=======================================')
'''

session_data = r.get(redis_session_key)
print('--------- list all keys -- decoded val------------------------------')
decoded_val = pickle.loads(session_data)
print(decoded_val)
print('--------- list all keys -- decoded val------------------------------')

dmtool_userid = decoded_val['dmtool_userid']
print('lal : dmtool_userid >>>>>>>>>>>>' , dmtool_userid)
