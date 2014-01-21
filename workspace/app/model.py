from datetime import datetime
from flaskext.sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(), unique=True)
    type = db.Column(db.String())
    web_user = db.Column(db.String())
    web_pwd = db.Column(db.String())
    naviseccli_user = db.Column(db.String())
    naviseccli_pwd = db.Column(db.String())
    rdp_user = db.Column(db.String())
    rdp_pwd = db.Column(db.String())
    ra_user = db.Column(db.String())
    ra_pwd = db.Column(db.String())
    putty_user = db.Column(db.String())
    putty_pwd = db.Column(db.String())
    ring_id = db.Column(db.Integer, db.ForeignKey('ring.id'))
    #ring = db.relationship('Ring', backref='host',lazy='dynamic')
    #ring = 
    def __init__(self, hostname, type=None, web_user = 'GlobalAdmin', web_pwd = 'password', \
                 naviseccli_user = 'GlobalAdmin', naviseccli_pwd = 'password', rdp_user = 'Administrator',\
                 rdp_pwd = 'clariion', ra_user= 'clariion1992', ra_pwd= 'clariion1992',\
                 putty_user = 'clariion1992', putty_pwd = 'clariion1992', ring_id = 1):
        self.hostname = hostname
        self.type = type
        self.web_user = web_user
        self.web_pwd = web_pwd
        self.naviseccli_user = naviseccli_user
        self.naviseccli_pwd = naviseccli_pwd
        self.rdp_user = rdp_user
        self.rdp_pwd = rdp_pwd
        self.ra_user = ra_user
        self.ra_pwd = ra_pwd
        self.putty_user = putty_user
        self.putty_pwd = putty_pwd
        self.ring_id = ring_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        
class Ring(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    hosts = db.relationship(Host, backref='ring',
                                lazy='dynamic')
  
    def __init__(self, name=None):
        self.name = name
  
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    
class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
   
    def __init__(self, name=None):
        self.name = name
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit() 
    
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    url = db.Column(db.String())
   
    def __init__(self, name=None, url=None):
        self.name = name
        if not url.startswith("http"):
            url = "http://" + url
        self.url = url
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit() 
         
class Ssh(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    host = db.Column(db.String(), unique=True)
    user = db.Column(db.String())
    pwd = db.Column(db.String())

    def __init__(self, name=None, host = None, user = None, pwd = None):
        self.name = name
        self.host = host
        self.user = user
        self.pwd = pwd

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()