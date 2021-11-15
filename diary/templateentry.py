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
    
    if request.method == 'POST':
        #retrieving data from page
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
        author     = flask.session["username"]

        #combining templated entries into content for database submission
        #formatting for easy viewing in diary
        content = ''
        if bp:
            content += ("Patient blood pressure: " + bp + '\n')
        if pulse:
            content += ("Patient pulse: " + pulse + '\n')
        if ox:
            content += ("Patient oxygen level: " + ox + '\n')
        if temp:
            content += ("Patient temperature: " + temp + '\n')
        if pain:
            content += ("Patient reported pain level: " + pain + '\n')
        if feel:
            content += ("Patient reported overall feeling: " + feel + '\n')
        if meds:
            content += ("Medicine administered to patient: " + meds + '\n')
        if diagnosis:
            content += ("Updated patient diagnosis: " + diagnosis + '\n')
        if procedures:
            content += ("New upcoming procedures: " + procedures + '\n')
        if goals:
            content += ("Goals for patient discharge: " + goals + '\n')
        
        #database submission
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO diary_entries
            (title, contents, author, diary_id)
            VALUES('{}', '{}', '{}', '{}')
        '''.format(title, content, author, 1))
        conn.commit()

        context = {'e': 1, 'message': 'Message submitted!'}
        return render_template('newentry.html', **context)

    #GET
    context = {'e': 0, 'message': ''}
    return render_template('templateentry.html')