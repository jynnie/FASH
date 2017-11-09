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
    completed = set()
    if user is not None:
        try:
            engine = create_engine('sqlite:///fash.db', echo=False)
            Session = sessionmaker(bind=engine)
            db = Session()

            all_com = db.query(Completed).filter(Completed.user==user.id, Completed.valid==True).all()
            for complete in all_com:
                completed.add(complete.task.id)
            db.close()
        except Exception as e:
            print('\n Failed to retrieve completed tasks :< are you logged in? \n')

    return render_template('play.html', user=user, tasks=tasks, completed=completed)

@app.route('/submit', methods=['GET', 'POST'])
@get_user()
def submit():
    if user is not None:
        complete = None
        try:
            engine = create_engine('sqlite:///fash.db', echo=False)
            Session = sessionmaker(bind=engine)
            db = Session()

            task_id = int(request.args.get('task'))
            task = db.query(Tasks).filter(Tasks.id == task_id).first()
        except Exception as e:
            return render_template('error.html', error="Sorry... we can't seem to find this task", user=user)
        try:
            complete = db.query(Completed).filter(Completed.user==user.id, Completed.task_name == task.id).first()
        except Exception as e:
            print("Has not completed this task before")

        if request.method == 'POST':
            try:
                link = request.form['link']
                if complete is not None:
                    if link == '' or link == ' ':
                        complete.valid = False
                    else:
                        complete.valid = True
                    complete.link = link
                    db.commit()
                else:
                    this_user = db.query(Users).filter(Users.email == user.email).first()
                    if link == '' or link == ' ':
                        completion = Completed(player=this_user, task=task, link=link, valid=False)
                    else:
                        completion = Completed(player=this_user, task=task, link=link, valid=True)
                    db.add(completion)
                    db.commit()

                if link == ' ' or link == '':
                    message = "Successfully removed submission!"
                else:
                    message = 'Added link successfully! Check the preview to make sure it worked.'
                return render_template('submit.html', user=user, task=task, complete=complete, message=message)
            except Exception as e:
                return render_template('submit.html', user=user, task=task, complete=complete, message='Something went wrong :(')

        return render_template('submit.html', user=user, task=task, complete=complete)
    else:
        return render_template('error.html', error="You need to login first >:(", user=None)
