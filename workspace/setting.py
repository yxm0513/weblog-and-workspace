import os
# configuration

ROOT = os.getcwd()
DEBUG = True
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
DEBUG_TB_INTERCEPT_REDIRECTS = False 
DB = r'/db/app.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + ROOT + DB
ADMIN = ['Simon', 'simon.yang.sh@gmail.com']
CSRF_ENABLED = False

SERVICES = {
            "Web": 8000,
            "Remote Desktop": 3389,
            "Remotely Anywhere": 9519,
            "putty": 23
            }