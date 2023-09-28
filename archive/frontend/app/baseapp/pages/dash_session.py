import dash
from dash import html, dcc, callback, Output, Input
#from flask import session
from app import session
import redis

import requests

import flask

#import libraries.formlibrary as fl
#from app.baseapp.libraries import formlibrary as fl

dash.register_page(__name__, path='/dash_session')

data_here = html.Div(id='div2',children=['data here'])
submit_button = html.Button('Submit', id='submit-val', n_clicks=0)

import dash_bootstrap_components as dbc
from dash import html

import chardet

def getcurrentuser(current_session_data_in):
        
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

row1 = html.Div(
    [
        dbc.Row(dbc.Col(data_here))
    ]
)

row2 = html.Div(
    [
        dbc.Row(dbc.Col(submit_button))
    ]
)

row = html.Div(
    [
        dbc.Row(dbc.Col(data_here)),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(submit_button),
            ]
        ),
    ]
)

layout = row

@callback(
	Output('div2', 'children'),
	Input('submit-val', 'n_clicks'))
def getvalue(clicks_in):
	return_value = {}
	#print((flask.request.cookies))
	#print((flask.request.cookies['session']))
	cookie = flask.request.cookies.get('session')
	print("cookie text >>>> ", cookie)
	session_cookie = "session:" + cookie

	r = redis.StrictRedis(host='container_redis_1', port=6379, db=0)
	all_keys = r.keys('*')
	#print(all_keys)
	print(type(all_keys))
	for k in all_keys:
	    val = r.get(k)
	    print(k)
	    print('---------------------------------------')
	    print(val)
	    print('=======================================')
		
	#first = all_keys[0]
	#val = r.get('session:3d6eaeb7-c227-4444-ac90-208da7732203')
	val = r.get(session_cookie)
	print('current session cookie >>>>>>>', val)
	current_user = getcurrentuser(val)
	print('current user  >>>>>', current_user)
	#sessionSession = requests.Session()
	#print("sessionSession >>>>>>>>" , sessionSession.cookies.get_dict())
	
	if not session:
		return_value = html.Div(id='div2',children=['no session data'])
	else:
		for key, value in session.items():
	              return_value[key] = value
	return return_value
