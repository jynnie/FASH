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
                    new_points = request.form['new_points']

                    task = Tasks(name = new_task, value = new_points, active = True)

                    db.add(task)
                    db.commit()

                    return redirect('/admin')

                except Exception as e:
                    print('Failed to change family!')

                    return render_template('edit.html', user=user, error='Failed to change family :< try again?')

            return render_template('admin.html', tasks=tasks)
    return render_template('error.html', login_url=DOMAIN + '/login', error="You don't have access to this page", user=None)
