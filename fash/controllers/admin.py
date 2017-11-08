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

@app.route('/admin', methods=['GET', 'POST'])
@get_user_and_tasks()
def admin():
    if user is not None:
        if user.email in config.ADMINS:
            if request.method == 'POST':
                try:
                    engine = create_engine('sqlite:///fash.db', echo=False)
                    Session = sessionmaker(bind=engine)
                    db = Session()

                    new_task = request.form['new_task']
                    new_value = request.form['new_points']

                    task = Tasks(name = new_task, value = new_value, active = True)

                    db.add(task)
                    db.commit()

                    return redirect('/admin')

                except Exception as e:
                    print('Failed to change family!')

                    return render_template('edit.html', user=user, error='Failed to change family :< try again?')

            return render_template('admin.html', user=user, tasks=tasks)
    return render_template('error.html', login_url=DOMAIN + '/login', error="You don't have access to this page", user=None)

@app.route('/edittask', methods=['GET', 'POST'])
@get_user()
def edit_task():
    if user is not None:
        if user.email in config.ADMINS:
            engine = create_engine('sqlite:///fash.db', echo=False)
            Session = sessionmaker(bind=engine)
            db = Session()

            task_id = int(request.args.get('task'))
            task = db.query(Tasks).filter(Tasks.id == task_id).first()

            if request.method == 'POST':
                try:
                    edit_task = request.form['name']
                    edit_value = request.form['value']
                    edit_active = request.form['active']

                    task.name = edit_task
                    task.value = edit_value
                    task.active = edit_active

                    db.commit()

                    return render_template('task.html', user=user, task=task, message='Success!! C:')

                except Exception as e:
                    print('Failed to change family!')

                    return render_template('task.html', user=user, task=task, message='Failed to edit task :< try again?')

            return render_template('task.html', user=user, task=task)
    return render_template('error.html', login_url=DOMAIN + '/login', error="You don't have access to this page", user=None)

@app.route('/review', methods=['GET', 'POST'])
@get_user()
def review():
    if user is not None:
        if user.email in config.ADMINS:
            return 'review.html not yet implemented'
    return render_template('error.html', login_url=DOMAIN + '/login', error="You don't have access to this page", user=None)