 def getcurrentemail(self,current_user_in):
        
        current_user_email = 'unknown@unknown.com'
        email_domain = 'unknown.com'
        
        print('============================================================')
        current_date = datetime.now()
        print(current_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        print('==================request data==============================')
        
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT id, email, username, active, confirmed_at FROM data.`user` where fs_uniquifier = %s" \
                       , (current_user_in,)) ## , is important
        
        try:
            user_details = cursor.fetchall()
            for row in user_details:
                current_user_email = row["email"]
            cursor.close()
            #session['dmtool_email_address'] = current_user_email
            #print('current user email > ' , current_user_email)
            email_domain = current_user_email.split('@')[1]
            #print('email domain > ', email_domain)
        except OSError as err:
            print("OS error:", err)
        except ValueError:
            print("Could not convert data to an integer.")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        except:
            current_user_email = 'unknown'
            email_domain = 'unknown'
        
        
        return current_user_email, email_domain
    
    def getcurrentuser(self,current_session_data_in):
        
        ##data = b"\x95\xc3\x8a\xb0\x8ds\x86\x89\x94\x82\x8a\xba"
        detected = chardet.detect(current_session_data_in)
        #print(detected["encoding"])
        decoded_current_session_data = current_session_data_in.decode(detected["encoding"])
        #print('decoded_current_session_data string')
        #print('-------------here----------------')
        #print(decoded_current_session_data)
        #print('------------to here--------------')
        
        all_values = []
        user_id = []
        
        splt = decoded_current_session_data.split('”Œ')
        
        next_value = 0
        
        for s in splt:
            s1 = s.split('Œ')
            for l1 in s1:
                if next_value == 1:
                    user_id.append(l1)
                    next_value = 0
                if 'user' in l1:
                    next_value = 1
                all_values.append(l1)
        try:
            current_user_from_cookie = user_id[0].lstrip()
        except:
            current_user_from_cookie = 'No user'
        
        
        #print('________all____________')
        #print(all_values)
        #print('________current_user_from_cookie____________')
        #print(current_user_from_cookie)
        
        return current_user_from_cookie
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
        
        '''
        return current_user_from_cookie
    
    def getcookiedata(self, environ_in):
        
        http_cookie = environ_in['HTTP_COOKIE']
        
        import os

        handler = {}

        #cookies = os.environ['HTTP_COOKIE']
        cookies = http_cookie.split('; ')
        current_cookie = cookies[0]
        colon_cookie = current_cookie.replace("=",":")
        #print('colon cookie')
        #print(colon_cookie)
        
        for cookie in cookies:
            cookie = cookie.split('=')
            handler[cookie[0]] = cookie[1]

        #for k in handler:
        #    print(k + " = " + handler[k])
        #    print('--------------')
        
        
        #print(http_cookie)container_frontend_1
        #print('---------------------------')
        encoded_cookie = bytes(colon_cookie, 'Windows-1252')
        #str_1_encoded = bytes(str_1,'UTF-8')
        
        #print('encoded cookie')
        #print(encoded_cookie)
        
        current_session_data = self.redisserver.get(encoded_cookie)
        #print('current session data')
        ##current_session = 'session=3d6eaeb7-c227-4444-ac90-208da7732203'
        #current_session = b'session:3d6eaeb7-c227-4444-ac90-208da7732203'
        #print(current_session_data)
        #val = self.redisserver.get(current_session)
        
        #print('===================================')
        
        import chardet
        
        try:
            current_user = self.getcurrentuser(current_session_data)
        except OSError as err:
            print("OS error:", err)
        except ValueError:
            print("Could not convert data to an integer.")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        except:
            current_user = 'no user'
        
        try:
            current_user_email, email_domain = self.getcurrentemail(current_user)
        except OSError as err:
            print("OS error:", err)
        except ValueError:
            print("Could not convert data to an integer.")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        except:
            current_user_email = 'anon@unknowndomain.com'
            email_domain = 'unknowndomain.com'
            
        
        return current_session_data, current_user, current_user_email, email_domain
