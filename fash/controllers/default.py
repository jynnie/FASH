from fash import app
import fash.config as config
from fash.constants import *
from fash.utils import *

from flask import (
        render_template,
        session,
        flash,
        request,
        redirect,
        abort
    )

@app.route('/')
@app.route('/index')
@get_user()
def index():
    return render_template("home.html", user=user)

@app.route('/leaderboard')
def leaderboard():
    return 'leaderboard.html not yet implemented'

@app.route('/profile')
@get_user()
def profile():
    if user is not None:
        return render_template("profile.html", user=user)
    return render_template('error.html', login_url=DOMAIN + "/login", error="You need to login first >:(", user=None)
