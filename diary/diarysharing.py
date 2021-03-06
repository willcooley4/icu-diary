from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db
import diary
import flask
import smtplib, ssl

bp = Blueprint('diary_sharing', __name__)  # NOTE: url_prefix?


# allows nurse to make a new diary for patient
# input patient name, diary name, and emergency contact email
@bp.route('/diary_sharing/', methods = ["POST", "GET"])
def diary_sharing():
    if 'username' not in session:
        return redirect('/auth/login')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT user_type FROM users
        WHERE username = '{}'
    '''.format(session['username']))
    row = cur.fetchone()
    print(row)
    if row['user_type']  not in ['primary_contributor', 'contributor']:
        return 'Access Denied. Your account type does not have access to this page.', 401
    if request.method == 'POST':
        # Access form data
        email = request.form.get('email')
        diary_name = request.form.get('diary')
        message = """\
        Subject: ICU Diary Join Invitation

        {} has requested access to the diary '{}'.
        """.format(session['username'], diary_name)

        send_email(email, message)

    context = {'user_type': row['user_type']}

    return render_template('diarysharing.html', **context)


def send_email(recipient_email, message):

    port = 465  # For SSL
    password = 'WNhZu6KawLL2i6r'

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("icudiary5@gmail.com", password)
        sender_email = "icudiary5@gmail.com"

        server.sendmail(sender_email, recipient_email, message)


