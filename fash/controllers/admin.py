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
@get_user()
def admin():
    if user is not None:
        if user.email in config.ADMINS:
            return render_template('admin.html')
    return render_template('error.html', login_url=DOMAIN + '/login', error="You don't have access to this page", user=None)
