from fash import app
import fash.config as config
from fash.constants import *
from fash.utils import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fash.models.user import *

# Imports for OpenID
from oic import rndstr
from oic.utils.http_util import Redirect
from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime

from flask import (
        render_template,
        session,
        flash,
        request,
        redirect,
        abort
    )

engine = create_engine('sqlite:///fash.db', echo=True)

@app.route('/login')
def login_page():
    Session = sessionmaker(bind=engine)
    db = Session()

    # Compute redirect url
    if 'redirect' in request.args:
        redirect_url = DOMAIN+'/login?redirect=' + request.args['redirect']
    else:
        redirect_url = DOMAIN+'/login'

	# Check if already logged in
    if 'jwt' in request.cookies:
        try:
            id = decode_token(request.cookies['jwt'])
            user = db.query(Users).filter(User.id == id).first()
            return redirect('/')
        except Exception as e:
            pass

    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    error = ""

    try:
        if "code" in request.args and "state" in request.args and request.args["state"] == session["state"]:
            r = requests.post('https://oidc.mit.edu/token', auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
                               data={"grant_type": "authorization_code",
                                     "code": request.args["code"],
                                     "redirect_uri": redirect_url})
            auth_token = json.loads(r.text)["access_token"]
            r = requests.get('https://oidc.mit.edu/userinfo', headers={"Authorization": "Bearer " + auth_token})
            user_info = json.loads(r.text)
            if "email" in user_info and user_info["email_verified"] == True and user_info["email"].endswith("@mit.edu"):
                # Authenticated
                email = user_info["email"]
                name = user_info["name"]

                user = db.query(Users).filter(Users.email == email).first()
                if user is None:
                    # Initialize the user with a very old last_post time
                    user = Users(email=email, name=name)
                    db.add(user)
                    db.commit()

                token = encode_token(user)
                response = app.make_response(redirect('/'))
                if 'redirect' in request.args:
                    response = app.make_response(redirect(request.args['redirect']))

                response.set_cookie('jwt', token, expires=datetime.datetime.now()+datetime.timedelta(days=90))
                return response
            else:
                if not "email" in user_info:
                    error = "We need your email to work."
                else:
                    error = "Invalid Login."

        session["state"] = rndstr()
        session["nonce"] = rndstr()

        args = {
            "client_id": CLIENT_ID,
            "response_type": ["code"],
            "scope": ["email", "openid", "profile"],
            "state": session["state"],
            "nonce": session["nonce"],
            "redirect_uri": redirect_url
        }

        auth_req = client.construct_AuthorizationRequest(request_args=args)
        login_url = auth_req.request('https://oidc.mit.edu/authorize')

        if error == "":
            return redirect(login_url)
        else:
            return render_template('error_login.html', login_url=login_url, error=error, user=None)

    except Exception as e:
        print('there was an exception')
        session["state"] = rndstr()
        session["nonce"] = rndstr()

        args = {
            "client_id": CLIENT_ID,
            "response_type": ["code"],
            "scope": ["email", "openid", "profile"],
            "state": session["state"],
            "nonce": session["nonce"],
            "redirect_uri": DOMAIN+'/login'
        }

        auth_req = client.construct_AuthorizationRequest(request_args=args)
        login_url = auth_req.request('https://oidc.mit.edu/authorize')

        return render_template('error.html', login_url=login_url, error="rip that didn't work :(", user=None)

@app.route('/logout')
def logout():
    response = app.make_response(redirect('/'))
    response.set_cookie('jwt', '')
    return response
