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

@app.route('/rules')
@get_user()
def rules():
    return render_template('rules.html', user=user)
