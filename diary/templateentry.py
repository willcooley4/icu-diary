from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db
import diary
import flask

bp = Blueprint('template_entry', __name__)  # NOTE: url_prefix?


# allows user to make a new diary submission
# diary entry page for doctor and contributors
# allows for standard, templated, or media submissions
@bp.route('/template_entry/', methods = ["POST", "GET"])
def template_entry():
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
    if row['user_type']  not in ['admin', 'physician']:
        return 'Access Denied. Your account type does not have access to this page.', 401

    patients = []
    if row['user_type'] == 'physician':
        cur.execute('''
            SELECT diary_id FROM contributors
            WHERE contributor = '{}' 
        '''.format(session['username']))
        rows = cur.fetchall()
        for row in rows:
            cur.execute('''
                SELECT patient FROM diaries
                WHERE id = {}
            '''.format(row['diary_id']))
            username = cur.fetchone()['patient']
            patients.append(username)

    print(patients)
    
    if request.method == 'POST':
        # retrieving data from page
        title      = request.form.get('title')
        bp         = request.form.get('bp')
        pulse      = request.form.get('pulse')
        ox         = request.form.get('ox')
        temp       = request.form.get('temp')
        pain       = request.form.get('pain')
        feel       = request.form.get('feel')
        meds       = request.form.get('meds')
        diagnosis  = request.form.get('diagnosis')
        procedures = request.form.get('procedures')
        goals      = request.form.get('goals')
        patient    = request.form.get('patient')
        author     = flask.session["username"]
        
        # combining templated entries into content for database submission
        # formatting for easy viewing in diary
        content = ''
        if bp:
            content += ("Patient blood pressure: " + bp + "\n")
        if pulse:
            content += ("Patient pulse: " + pulse + "\n")
        if ox:
            content += ("Patient oxygen level: " + ox + "\n")
        if temp:
            content += ("Patient temperature: " + temp + "\n")
        if pain:
            content += ("Patient reported pain level: " + pain + "\n")
        if feel:
            content += ("Patient reported overall feeling: " + feel + "\n")
        if meds:
            content += ("Medicine administered to patient: " + meds + "\n")
        if diagnosis:
            content += ("Updated patient diagnosis: " + diagnosis + "\n")
        if procedures:
            content += ("New upcoming procedures: " + procedures + "\n")
        if goals:
            content += ("Goals for patient discharge: " + goals + "\n")

        
        cur.execute('''
            SELECT id 
            FROM diaries
            WHERE patient = '{}'
        '''.format(patient))
        row = cur.fetchone()

        if row == None:
            context = {'e': 2, 'message': 'Incorrect patient name or patient does not exist. Please try again.',
            'patients': patients}
            return render_template('templateentry.html', **context)
        diary_id = row['id']
        
        # database submission
        cur.execute('''
            INSERT INTO diary_entries
            (title, contents, author, diary_id)
            VALUES('{}', '{}', '{}', '{}')
        '''.format(title, content, author, diary_id))
        conn.commit()

        context = {'e': 1, 'message': 'Message submitted!', 'patients': patients}
        return render_template('templateentry.html', **context)

    # GET
    print(patients)
    context = {'e': 0, 'message': '', 'patients': patients}
    return render_template('templateentry.html', **context)