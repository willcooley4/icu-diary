# import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# from werkzeug.security import check_password_hash, generate_password_hash

# from diary.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Page for users to enter username, password to access the site
# All other pages but signup redirect here if not signed in
# Redirects to home once form submitted



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        pass
    else:  # GET
        return render_template('auth/login.html')

# Page for users to create a new account
# Redirects to home once form submitted
@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    # TODO
    return ''

# Page for users to log out of account
# Redirects to login once form submitted
@bp.route('/logout', methods=('POST',))
def logout():
    # TODO
    return ''
