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

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@get_user()
def index():
    return render_template("home.html", user=user)

@app.route('/profile')
def profile():
    return render_template("profile.html", user=user)
