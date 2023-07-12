import chardet

def getemail(current_session_data_in):
        
    ##data = b"\x95\xc3\x8a\xb0\x8ds\x86\x89\x94\x82\x8a\xba"
    detected = chardet.detect(current_session_data_in)
    #print(detected["encoding"])
    decoded_current_session_data = current_session_data_in.decode(detected["encoding"])
    #print('decoded_current_session_data string')
    #print('-------------here----------------')
    #print(decoded_current_session_data)
    #print('------------to here--------------')
    
    all_values = []
    email = []
    
    splt = decoded_current_session_data.split('”Œ')
    
    next_value = 0
    
    for s in splt:
        s1 = s.split('Œ')
        for l1 in s1:
            if next_value == 1:
                email.append(l1)
                next_value = 0
            if 'email' in l1:
                next_value = 1
            all_values.append(l1)
    try:
        current_email_from_cookie = email[0].lstrip()
    except:
        current_email_from_cookie = 'No email'
    
    
    print('________all____________')
    print(all_values)
    print('________current_email_from_cookie____________')
    print(current_email_from_cookie)
    
    return current_email_from_cookie
    '''
    
    ##decoded_utf8 = val.decode('Windows-1252').encode('utf-8','ignore')
    ##print(decoded_utf8)
    
    #print(ast.literal_eval(val.decode("utf-8","ignore")))
    
    ##session_data = self.redisserver.get(current_session)
    ##session_dict = json.loads(session_data.decode('utf-8','ignore'))
    
    #dict = json.loads(self.redisserver.get(current_session))
    ##print(session_dict)
    ##print('TTTTTTTTTTTTTTTTTTTTTTTT')
    ##dict = self.redisserver.hgetall(current_session)
    #print(val.decode("utf-8","ignore"))
    #print('--------------------------')
    #print(val)
    print('+++++++++++++++++++++++++++')
    #print(type(val))
    print('=============================')
    
    ##print(val['email'])
    
    ##all_keys = self.redisserver.keys('*')
    ##print(all_keys)
    
   
    return current_user_from_cookie
    '''

