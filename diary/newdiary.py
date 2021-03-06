from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from secrets import token_hex

from diary.db import get_db
from diary.auth import register_user
from diary.diarysharing import send_email

bp = Blueprint('new_diary', __name__)  # NOTE: url_prefix?


# allows nurse to make a new diary for patient
# input patient name, diary name, and emergency contact email
@bp.route('/new_diary/', methods = ["POST", "GET"])
def new_diary():
    if 'username' not in session:
        return redirect('/auth/login')
    # TODO: verify user is doctor or admin

    # retrieve database connection
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT user_type FROM users
        WHERE username = '{}'
    '''.format(session['username']))
    row = cur.fetchone()
    print(row)
    if row['user_type']  not in ['admin', 'physician']:
        return 'Access Denied. Your account type does not have access to this page.', 401

    user_type = row['user_type']


    if request.method == 'POST':

        # get form contents
        patient_name = request.form.get('patient_name')
        patient_email = request.form.get('patient_email')
        contact_name = request.form.get('contact_name')
        contact_email = request.form.get('contact_email')
        diary_name = request.form.get('diary_name')

        if patient_email == contact_email:
            context = {'user_type': user_type, 'e': 1, 'message': 'Patient and emergency contact email cannot match.'}
            return render_template('newdiary.html', **context)


        # register patient + email
        patient_username = patient_name.replace(" ", "").lower() + '_' + token_hex(4)
        patient_password = token_hex(8)
        register_user(patient_username, patient_password, patient_password, patient_name, patient_email, 'patient')
        message = """\
        Subject: ICU Diary Patient Registration

        {} has been registered as the patient for diary '{}'.
        Username: {}
        Password: {}
        """.format(patient_name, diary_name, patient_username, patient_password)
        send_email(patient_email, message)

        # create diary
        cur.execute('''
        INSERT INTO diaries(name, patient)
        VALUES ('{}', '{}') RETURNING id
        '''.format(diary_name, patient_username))
        diary_id = cur.fetchone()['id']

        #  register primary contributor + email
        # TODO: include contributor relation to diary
        contact_username = contact_name.replace(" ", "").lower() + '_' + token_hex(4)
        contact_password = token_hex(8)
        register_user(contact_username, contact_password, contact_password, contact_name, contact_email, 'primary_contributor')
        message = """\
        Subject: ICU Diary Contributor Registration

        {} has been registered as the primary contributor for diary '{}'.
        This is the ICU diary for patient: {}
        Username: {}
        Password: {}
        """.format(contact_name, diary_name, patient_name, contact_username, contact_password)

        cur.execute('''
        INSERT INTO contributors(contributor, diary_id, primary_contributor, approved)
        VALUES ('{}', '{}', TRUE, TRUE)
        '''.format(contact_username, diary_id))
        conn.commit()
        send_email(contact_email, message)

        cur.execute('''
            INSERT INTO contributors(contributor, diary_id, approved, primary_contributor)
            VALUES('{}', '{}', TRUE, FALSE)
        '''.format(session['username'], diary_id))
        conn.commit()

    context = {'user_type': user_type}
    return render_template('newdiary.html', **context)
