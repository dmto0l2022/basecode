from flask import current_app
from flask_security import Security, current_user, auth_required, SQLAlchemySessionUserDatastore

##https://stackoverflow.com/questions/14793098/how-to-use-flask-security-register-view
current_app.config['SECURITY_REGISTERABLE'] = True
current_app.config['SECURITY_REGISTER_URL'] = '/app/register'
current_app.config['SECURITY_LOGIN_URL'] = '/app/login'
current_app.config['SECURITY_LOGOUT_URL'] = '/app/logout'
current_app.config['SECURITY_RESET_URL'] = '/app/reset'
current_app.config['SECURITY_CHANGE_URL'] = '/app/change'
current_app.config['SECURITY_CONFIRM_URL'] = '/app/confirm'
current_app.config['SECURITY_POST_LOGIN_VIEW'] = '/app/welcome'
current_app.config['SECURITY_POST_LOGOUT_VIEW'] = '/app/login'
current_app.config['SECURITY_POST_REGISTER_VIEW'] = '/app/welcome'
current_app.config['SECURITY_POST_CONFIRM_VIEW'] = '/app/welcome'
current_app.config['SECURITY_POST_RESET_VIEW'] = '/app/welcome'
current_app.config['SECURITY_POST_CHANGE_VIEW'] = '/app/welcome'
current_app.config['SECURITY_UNAUTHORIZED_VIEW'] = '/app/register'
current_app.config['SECURITY_CONFIRMABLE'] = True
current_app.config['SECURITY_RECOVERABLE'] = True
current_app.config['SECURITY_TRACKABLE='] = True
current_app.config['SECURITY_CHANGEABLE'] = True

