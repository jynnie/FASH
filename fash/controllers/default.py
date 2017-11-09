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
    message = ''
    completed = []
    try:
        engine = create_engine('sqlite:///fash.db', echo=False)
        Session = sessionmaker(bind=engine)
        db = Session()

        completed = db.query(Completed).filter(Completed.valid==True, Completed.user != None).all()
    except Exception as e:
        message = "Sorry, we can't load pictures right now :( Let us know about this problem!"

    return render_template("home.html", user=user, message=message, completed=completed)

@app.route('/rules')
@get_user()
def rules():
    return render_template('rules.html', user=user)
