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

    # retrieve database connection
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
        SELECT user_type FROM users
        WHERE username = '{}'
    '''.format(session['username']))
    row = cur.fetchone()
    print(row)
    if row['user_type']  not in ['admin', 'primary_contributor']:
        return 'Access Denied. Your account type does not have access to this page.', 401

    if request.method == 'POST':
        # Access form data
        print(request.form)
        if 'email' in request.form:
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

        elif 'approve' in request.form:
            user = request.form.get('approve')
            cur.execute('''
                UPDATE contributors
                SET approved = TRUE
                WHERE contributor = '{}'
            '''.format(user))
            conn.commit()
        elif 'deny' in request.form:
            user = request.form.get('deny')
            cur.execute('''
                DELETE FROM contributors
                WHERE contributor = '{}'
            '''.format(user))
            conn.commit()
        else:
            return '400 Bad Request', 400

    # TODO: select correct diary_id
    cur.execute('''
        SELECT * FROM contributors
        WHERE diary_id = '{}' AND approved = FALSE
    '''.format(1))
    rows = cur.fetchall()
    print(rows)

    context = {'users': rows}

    # TODO: add closable info message when thing is submitted
    return render_template('invite.html', **context)