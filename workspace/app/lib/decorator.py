# -*- coding: utf-8 -*-
"""
    lib/decorator.py
    ~~~~~~~~~~~~~~

    some decorator defined

"""
from functools import wraps
from flask import session, redirect, url_for, flash, request, make_response
#from models.user import User
#from util import helper

#def login_required(f):
#
#    @wraps(f)
#    def do(*args, **kwargs):
#        if 'userId' not in session:
#            #cookie自动登录机制
#            token=request.cookies.get('auto_login')
#            if token:
#                userId, token = token.split('_')
#                user = User.get_user_by_id(userId)
#                from matrix import app
#                if user and helper.md5(str(user.id) + user.password + app.config['SECURIY_KEY'])==token:
#                    session['userId']=user.id
#                    session['phone']=user.phone
#                    session['nickName']=user.nickName
#                else:
#                    return redirect('/logout')
#            else:
#                return redirect('/')
#
#        return f(*args, **kwargs)
#
#    return do

def no_cache_header(f):

    @wraps(f)
    def do(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.headers['pragma'] = 'no-cache'
        response.headers['Cache-Control'] = 'no-cache, must-revalidate'
        return response
    return do