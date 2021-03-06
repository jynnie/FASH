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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fash.models.user import *

@app.route('/profile')
@get_user()
def profile():
    if user is not None:
        completed = set()
        points = 0
        try:
            engine = create_engine('sqlite:///fash.db', echo=False)
            Session = sessionmaker(bind=engine)
            db = Session()

            completed = db.query(Completed).filter(Completed.user==user.id, Completed.valid==True).all()

            for complete in completed:
                points += complete.task.value
        except Exception as e:
            print('\n Failed to retrieve completed tasks :< are you logged in? \n')
            return render_template('error.html', error = 'Failed to retrieve completed tasks :<', user=user)

        return render_template("profile.html", user=user, completed=completed, points=points)
    return render_template('error.html', login_url=DOMAIN + "/login", error="You need to login first >:(", user=None)

@app.route('/edit', methods=['GET', 'POST'])
@get_user()
def edit():
    if user is not None:
        if request.method == 'POST':
            try:
                engine = create_engine('sqlite:///fash.db', echo=False)
                Session = sessionmaker(bind=engine)
                db = Session()

                family = request.form['family']

                new_user = db.query(Users).filter(Users.email == user.email).first() # Get current user (can't edit from user itself - conflicting sessions)
                new_family = db.query(Families).filter(Families.name == family).first() # Get family
                new_user.fam_mem = new_family # Set family of user
                db.commit()

                return redirect('/profile')

            except Exception as e:
                print('Failed to change family!')

                return render_template('edit_profile.html', user=user, error='Failed to change family :< try again?')

        return render_template('edit_profile.html', user=user)
    else:
        return render_template('error.html', login_url=DOMAIN + "/login", error="You need to login first >:(", user=None)
