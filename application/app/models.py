# model.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Table, LargeBinary, DateTime, Boolean,UnicodeText

from flask_dance.consumer.storage.sqla import SQLAlchemyStorage , OAuthConsumerMixin

from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref

from . import db ## import db from __init__

# must be defined after db = SQLAlchemy_bind() if in same module
# from sqlalchemy import Column, Integer, String

class RolesUsers(db.Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(db.Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(UnicodeText)



class GoogleUser(db.Base, UserMixin):
    __tablename__ = 'google_users'
    id = Column(Integer, primary_key=True)
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    email = Column(String(256), unique=True)
    name = Column(String(256))


class OAuth(OAuthConsumerMixin, db.Base):
    __tablename__ = 'oauth'
    provider_user_id = Column(String(256), unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(GoogleUser)

class User(db.Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    '''
    def set_self(self, id, email, username, password, last_login_at,):
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.last_login_at = last_login_at
        self.current_login_at = current_login_at
        self.last_login_ip = last_login_ip
        self.current_login_ip = current_login_ip 
        self.login_count = login_count
        self.active = active
        self.fs_uniquifier = fs_uniquifier
        self.confirmed_at = confirmed_at
        self.roles = roles
    '''
    @staticmethod
    def get_username(fs_uniquifier_in):
        """
        :return: list of user details
        """
        #username_out = User.query(User.username).filter_by(fs_uniquifier==fs_uniquifier_in).first()
        
        #peter = User.query.filter_by(username='peter').first()
        #peter.id
        #peter.email
        
        user_out = User.query.filter(User.fs_uniquifier==fs_uniquifier_in).first()
        username_out = user_out.username
        
        return username_out
    
    @staticmethod
    def get_user(fs_uniquifier_in):
        """
        :return: list of user details
        """
        #username_out = User.query(User.username).filter_by(fs_uniquifier==fs_uniquifier_in).first()
        
        #peter = User.query.filter_by(username='peter').first()
        #peter.id
        #peter.email
        
        user_out = User.query.filter(User.fs_uniquifier==fs_uniquifier_in).first()
               
        return user_out

class Session(db.Base):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), unique=True)
    data = Column(LargeBinary)
    expiry = Column(DateTime)

    def __init__(self, session_id, data, expiry):
        self.session_id = session_id
        self.data = data
        self.expiry = expiry

    def __repr__(self):
        return '<Session data %s>' % self.data

class User_new(db.Base):
    __tablename__ = 'users_new'
    id = Column(Integer, primary_key=True)
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    username = Column(String(25), unique=True)
    password = Column(String(25), unique=True)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

# User table
class UserSimple(db.Base):
    __tablename__ = "users_simple"
    id = Column(Integer, primary_key=True)
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    username = Column(String(25))
    name = Column(String(25))
    email = Column(String(25))

    def __init__(self, username: str, name: str, email: str):
        self.username = username
        self.name = name
        self.email = email

    @staticmethod
    def create(username, name, email):
        """
        Create new user
        """
        new_user = User(username, name, email)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_users():
        """
        :return: list of user details
        """
        users = [
            {
                'user_id': i.id,
                'username': i.username,
                'name': i.name,
                'email': i.email,
            }
            for i in UserSimple.query.order_by('id').all()
        ]
        return users

# Plots table
class Plots(db.Base):
    __tablename__ = "plots"
    id = Column(Integer, primary_key=True)
    plotid = Column(String(25))
    name = Column(String(25))

    def __init__(self, plotid: str, name: str):
        self.plotid = plotid
        self.name = name

    @staticmethod
    def create(plotid,name):
        """
        Create new plot
        """
        new_plots = Plots(plotid,name)
        db.session.add(new_plots)
        db.session.commit()

    @staticmethod
    def getall():
        """
        :return: list of user details
        """
        plots = [
            {
                'id': i.id,
                'plotid': i.plotid,
                'name': i.name,
            }
            for i in Plots.query.order_by('id').all()
        ]
        return plots
    
    @staticmethod
    def read(plotid_in):
        """
        :return: one plot
        """
        #oneplot = Plots.query.filter(Plots.plotid.in_((plotid_in)))
        oneplot = Plots.query.filter_by(plotid=plotid_in)
        return oneplot

    @staticmethod
    def update(plotid_in, newname_in):
        num_rows_updated = Plots.query.filter_by(plotid=plotid_in).update(dict(name=newname_in))
        db.session.commit()
        
    @staticmethod
    def delete(plotid_in):
        num_rows_deleted = Plots.query.filter_by(plotid=plotid_in).delete()
        db.session.commit()
    
