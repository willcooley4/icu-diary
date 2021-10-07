# import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# from werkzeug.security import check_password_hash, generate_password_hash

from diary.db import get_db
import uuid
import hashlib

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Page for users to enter username, password to access the site
# All other pages but signup redirect here if not signed in
# Redirects to home once form submitted
@bp.route('/login', methods=('GET', 'POST'))
def login():
    # TODO: modify for hashed and salted passwords
    # TODO: start session on login
    # TODO: redirect if logged in
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
        row = cur.fetchone()

        # check username exists
        if row == None:
            context = {'e': 1, 'message': 'Username does not exist.'}
            return render_template('auth/login.html', **context)

        # modify input and stored password for hash comparison
        stored_pass = row['password'].split('$')
        salted_input = stored_pass[1] + password
        hashed_obj = hashlib.new(stored_pass[0])
        hashed_obj.update(salted_input.encode('utf-8'))
        hashed_input = hashed_obj.hexdigest()

        # Check if valid password
        if row['password'] != '$'.join([stored_pass[0], stored_pass[1], hashed_input]):
            context = {'e': 1, 'message': 'Password does not match username.'}
            return render_template('auth/login.html', **context)

        # Log user in on success, redirect to home page
        session['username'] = row['username']
        return redirect('/')

    # GET
    context = {'e': 0, 'message': ''}
    return render_template('auth/login.html', **context)

# Page for users to create a new account
# Redirects to home once form submitted
@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    # TODO: referral way
    # TODO: link to diary
    # TODO: handle profile picture upload
    # TODO: include email
    if 'username' in session:
        return redirect('/')
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
            context = {'e': 1, 'message': 'Passwords do not match.'}
            return render_template('auth/signup.html', **context)

        # check that username is not taken
        cur.execute('''
            SELECT username FROM users
            WHERE username = '{}'
        '''.format(username))
        row = cur.fetchone()
        if row != None and row['username'] == username:
            context = {'e': 1, 'message': 'Username already exists.'}
            return render_template('auth/signup.html', **context)

        # Modify password for storage
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new('sha512')
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join(['sha512', salt, password_hash])

        print(password_db_string)
        # Create user account
        cur.execute('''
            INSERT INTO users(username, full_name, password, profile_pic)
            VALUES ('{}', '{}', '{}', '{}')
        '''.format(username, fullname, password_db_string, 'lala.jpg'))
        conn.commit()

        # Start user session
        session['username'] = username

        return redirect('/')
    # GET
    context = {'e': 0, 'message': ''}
    return render_template('auth/signup.html', **context)

# Page for users to log out of account
# Redirects to login once form submitted
@bp.route('/logout', methods=('POST','GET'))
def logout():
    session.pop('username', None)
    return redirect('/auth/login')
