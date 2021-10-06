# import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# from werkzeug.security import check_password_hash, generate_password_hash

from diary.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Page for users to enter username, password to access the site
# All other pages but signup redirect here if not signed in
# Redirects to home once form submitted
@bp.route('/login', methods=('GET', 'POST'))
def login():
    # TODO: modify for hashed and salted passwords
    # TODO: start session on login
    # TODO: redirect if logged in
    # TODO: login error headers
    if request.method == 'POST':
        # Access form data
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM users
            WHERE username = '{}'
        '''.format(username))
        pw_check = cur.fetchone()['password']
        if(pw_check == password):
            return 'welcome ' + username
        else:
            return 'denied'
    # GET
    return render_template('auth/login.html')

# Page for users to create a new account
# Redirects to home once form submitted
@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    # TODO: referral way
    # TODO: link to diary
    # TODO: redirect if already logged in
    # TODO: start session
    # TODO: creation error headers
    if request.method == 'POST':
        # Access form data
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        fullname = request.form.get('fullname')
        email = request.form.get('email')

        conn = get_db()
        cur = conn.cursor()

        # check if both password entries match
        if password != password2:
            return '400: passwords do not match'

        # check that username is not taken
        cur.execute('''
            SELECT username FROM users
            WHERE username = '{}'
        '''.format(username))
        row = cur.fetchone()
        if row != None and row['username'] == username:
            return '400: username already exists'

        return username + password + password2 + fullname + email
    # GET
    return render_template('auth/signup.html')

# Page for users to log out of account
# Redirects to login once form submitted
@bp.route('/logout', methods=('POST',))
def logout():
    # TODO
    return 'logout'
