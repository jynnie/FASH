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

@app.route('/play', methods=['GET'])
@get_user_and_tasks()
def play():
    try:
        engine = create_engine('sqlite:///fash.db', echo=False)
        Session = sessionmaker(bind=engine)
        db = Session()

        all_tasks = db.query(Completed).filter(Completed.user==user.id).all()
        completed = set()
        for task in all_tasks:
            completed.add(task.id)
    except Exception as e:
        print('\n Failed to retrieve completed tasks :< \n')

    return render_template('play.html', user=user, tasks=tasks, completed=completed)

@app.route('/submit', methods=['GET'])
@get_user()
def submit():
    return 'submit.html not yet implemented'
