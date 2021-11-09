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
    if request.method == 'POST':
        # Access form data
        email = request.form.get('email')
        diary_name = request.form.get('diary')
        message = """\
        Subject: Hi there

        This message is sent from Python.
        {} has requested access to the diary '{}'.
        """.format(session['username'], diary_name)

        send_email(email, message)

    return render_template('diarysharing.html')


def send_email(recipient_email, message):

    port = 465  # For SSL
    password = 'WNhZu6KawLL2i6r'

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("icudiary5@gmail.com", password)
        sender_email = "icudiary5@gmail.com"

        server.sendmail(sender_email, recipient_email, message)


