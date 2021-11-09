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

    if request.method == 'POST':
        # get form contents
        patient_name = request.form.get('patient_name')
        patient_email = request.form.get('patient_email')
        contact_name = request.form.get('contact_name')
        contact_email = request.form.get('contact_email')
        diary_name = request.form.get('diary_name')

        # TODO: register patient + email
        print(patient_name.replace(" ", "").lower() + '_' + token_hex(4))
        print(patient_name.replace(" ", "").lower())
        print(patient_name.replace(" ", ""))
        print(patient_name)
        patient_username = patient_name.replace(" ", "").lower() + '_' + token_hex(4)
        patient_password = token_hex(16)
        register_user(patient_username, patient_password, patient_password, patient_name, patient_email, 'patient')
        patient_message = """\
        Subject: Hi there

        This message is sent from Python.
        {} has been registered as the patient for diary '{}'.
        Username: {}
        Password: {}
        """.format(patient_name, diary_name, patient_username, patient_password)
        send_email(patient_email, patient_message)
        # TODO: register primary contributor + email
        # TODO: create diary
    
    return render_template('newdiary.html')
