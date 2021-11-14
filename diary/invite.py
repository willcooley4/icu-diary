from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db
from diary.diarysharing import send_email


bp = Blueprint('invite', __name__)  # NOTE: url_prefix?

@bp.route('/invite', methods=('GET', 'POST'))
def invite():
    if 'username' not in session:
        return redirect('/auth/login')
    
    # TODO: verify that user is primary contributor

    # retrieve database connection
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        # Access form data
        email = request.form.get('email')

        cur.execute('''
            SELECT diary_id FROM contributors
            WHERE contributor = '{}'
        '''.format(session['username']))
        diary_id = cur.fetchone()['diary_id']
        cur.execute('''
            SELECT * FROM diaries
            WHERE id = '{}'
        '''.format(diary_id))
        row = cur.fetchone()

        # TODO: use names, not usernames
        message = """\
        Subject: Hi there

        This message is sent from Python.
        {} has invited you to contribute to {}'s diary.
        Use diary_id {} to register after creating an account at: https://icu-diary-495.herokuapp.com/auth/signup
        """.format(session['username'], row['name'], diary_id)
        send_email(email, message)

    cur.execute('''
        SELECT * FROM contributors
        WHERE diary_id = '{}' AND approved = FALSE
    '''.format(1))
    rows = cur.fetchall()
    print(rows)

    context = {'users': rows}


    return render_template('invite.html', **context)