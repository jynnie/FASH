import uuid
import jwt
import os
from fash.config import *
from fash.constants import *
from fash.models.user import *
from flask import (redirect, request)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps
import datetime

def gen_uuid():
    return str(uuid.uuid4()).replace('-', '')

def encode_token(user):
    return jwt.encode({'id': user.id, 'email': user.email, 'roll': gen_uuid()}, SECRET, algorithm='HS256')

def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=['HS256'])['id']


epoch = datetime.datetime(1970, 1, 1)
def epoch_seconds(date):
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def requires_auth():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            engine = create_engine('sqlite:///fash.db', echo=True)
            Session = sessionmaker(bind=engine)
            db = Session()

            if 'jwt' in request.cookies:
                try:
                    decoded = decode_token(request.cookies['jwt'])
                except Exception as e:
                    return redirect('/login?redirect='+request.url)
                user = db.query(Users).filter(Users.id==decoded).first()
                f.__globals__['user'] = user
                return f(*args, **kwargs)
            else:
                return redirect('/login')

        return decorated
    return decorator

def get_user():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            engine = create_engine('sqlite:///fash.db', echo=True)
            Session = sessionmaker(bind=engine)
            db = Session()
            if 'jwt' in request.cookies:
                try:
                    decoded = decode_token(request.cookies['jwt'])
                except Exception as e:
                    # FIXME Repeated code
                    f.__globals__['user'] = None
                    return f(*args, **kwargs)
                user = db.query(Users).filter(Users.id==decoded).first()
                f.__globals__['user'] = user
                return f(*args, **kwargs)
            else:
                f.__globals__['user'] = None
                return f(*args, **kwargs)

        return decorated
    return decorator

def get_user_and_tasks():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            engine = create_engine('sqlite:///fash.db', echo=True)
            Session = sessionmaker(bind=engine)
            db = Session()

            if 'jwt' in request.cookies:
                try:
                    decoded = decode_token(request.cookies['jwt'])
                    user = db.query(Users).filter(Users.id==decoded).first()
                    f.__globals__['user'] = user
                except Exception as e:
                    # FIXME Repeated code
                    f.__globals__['user'] = None
            else:
                f.__globals__['user'] = None

            tasks = db.query(Tasks).filter(Tasks.active == True).all()
            f.__globals__['tasks'] = tasks
            return f(*args, **kwargs)

        return decorated
    return decorator

def requires_auth_s():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = args[0]
            if 'jwt' in data:
                engine = create_engine('sqlite:///fash.db', echo=True)
                Session = sessionmaker(bind=engine)
                db = Session()
                try:
                    decoded = decode_token(data['jwt'])
                except Exception as e:
                    disconnect()
                    return
                user = db.query(Users).filter(Users.id==decoded).first()
                kwargs['user'] = user
                return f(*args, **kwargs)
            else:
                disconnect()
                return

        return decorated
    return decorator

def val_form_keys(keys):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            for key in keys:
                if not key in request.form:
                    return "Missing: " + key, 400
                kwargs[key] = request.form[key]
            return f(*args, **kwargs)

        return decorated
    return decorator

def get_ts(dt):
    return (dt-datetime.datetime(1970,1,1)).total_seconds()
