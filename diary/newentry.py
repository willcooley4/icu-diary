from logging import FileHandler
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db
import diary
import flask

bp = Blueprint('entry_page', __name__)  # NOTE: url_prefix?


# allows user to make a new diary submission
# diary entry page for doctor and contributors
# allows for standard, templated, or media submissions
@bp.route('/entry_page/', methods = ["POST", "GET"])
def entry_page():
    # access form data
    if 'username' not in session:
        return redirect('/auth/login')
    

    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
        SELECT user_type FROM users
        WHERE username = '{}'
    '''.format(session['username']))
    row = cur.fetchone()

    user_type = row['user_type']

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        media = request.form.get('media')
        author = flask.session["username"]
        
        #get diary_id
        if user_type != 'physician':
            cur.execute('''
                SELECT diary_id
                FROM contributors
                WHERE contributor = '{}'
            '''.format(session['username']))
            diary_id = cur.fetchone()['diary_id']
        else:
            patient = request.form.get('patient')
            cur.execute('''
                SELECT id 
                FROM diaries
                WHERE patient = '{}'
            '''.format(patient))
            row = cur.fetchone()

            if row == None:
                context = {'e': 2, 'message': 'Incorrect patient name or patient does not exist. Please try again.', 'user_type': user_type}
                return render_template('newentry.html', **context)
            diary_id = row['diary_id']


        # access database and submit diary entry
        cur.execute('''
            INSERT INTO diary_entries
            (title, contents, media, author, diary_id)
            VALUES('{}', '{}', '{}', '{}', '{}')
        '''.format(title, content, media, author, diary_id))
        conn.commit()

        context = {'e': 1, 'message': 'Message submitted!', 'user_type': user_type}
        return render_template('newentry.html', **context)

    
    #GET
    context = {'e': 0, 'message': '', 'user_type': user_type}
    return render_template('newentry.html', **context)

