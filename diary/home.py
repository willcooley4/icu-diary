from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db


bp = Blueprint('home', __name__)  # NOTE: url_prefix?

@bp.route('/', methods=('GET', 'POST'))
def home():
    if 'username' not in session:
        return redirect('/auth/login')

    # establish database connection
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM users
        WHERE username = '{}'
    '''.format(session['username']))
    user_type = cur.fetchone()['user_type']

    if request.method == 'POST':
        print('post worked :)')
        diary_id = request.form.get('diary_id')
        message = request.form.get('message')

        #check valid diaryid
        cur.execute('''
            SELECT id
            FROM diaries
            WHERE id = '{}'
        '''.format(diary_id))
        row = cur.fetchone()
        if row == None:
            context = {'e': 1, 'message': 'That Diary ID does not exist. Please try again.'}
            return render_template('unverified_home.html', **context)

        cur.execute('''
            INSERT INTO contributors(contributor, diary_id, approved, primary_contributor, message)
            VALUES('{}', '{}', FALSE, FALSE, '{}')
        '''.format(session['username'], diary_id, message))
        conn.commit()

    if user_type == 'contributor':
        cur.execute('''
            SELECT * FROM contributors
            WHERE contributor = '{}'
        '''.format(session['username']))
        print('in contributor')
        row = cur.fetchone()
        print(row)
        print(type(row))
        if not row:
            return render_template('unverified_home.html')
        if not row['approved']:
            print('this dude is unverified')
            return render_template('unverified_home.html')

    context = {} 
    print(user_type)
    if user_type == 'admin':
        # TODO: admin doesn't need all these links, just easier for debugging
        context['cards'] = ['write', 'share', 'create', 'requests', 'learn', 'admin']
    elif user_type == 'primary_contributor':
        context['cards'] = ['write', 'share', 'requests', 'learn']
    elif user_type == 'contributor':
        context['cards'] = ['write', 'share', 'learn']
    elif user_type == 'patient':
        context['cards'] = ['view', 'write', 'learn']
    elif user_type == 'physician':
        context['cards'] = ['write', 'create', 'learn']
    else:
        return 'Bad request: user_type does not exitst', 401

    return render_template('index.html', **context)