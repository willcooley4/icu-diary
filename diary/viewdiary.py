from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)

from diary.db import get_db
import diary
import flask
import os

from fpdf import FPDF


bp = Blueprint('view_diary', __name__)  # NOTE: url_prefix?

# scroll through diary entries
# posts sorted chronologically
# @bp.route('/view_diary/', methods = ["POST", "GET"])
# def view_diary():
#     if 'username' not in session:
#         return redirect('/auth/login')
#     return render_template('navbar.html')

@bp.route('/view_diary/', methods = ["POST", "GET"])
def view_diary():
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
    if row['user_type']  not in ['patient', 'admin']:
        return 'Access Denied. Your account type does not have access to this page.', 401

    cur.execute('''
        SELECT id
        FROM diaries
        WHERE patient = '{}'
    '''.format(session['username']))
    print(session['username'])
    diary_id = cur.fetchone()['id']
    print(diary_id)
    cur.execute('''
        SELECT * FROM diary_entries
        WHERE diary_id = '{}'
    '''.format(diary_id))
    rows = cur.fetchall()

    context = {'entries': rows}
    return render_template('viewdiary.html', **context)

@bp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):

    pdf = FPDF(format='Letter')
    pdf.add_page()
    txt = "ajdlkln weofjq  eknfaekwjfasdfhlkadfasd"
    pdf.set_font('Arial', '', 12)

    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT id
        FROM diaries
        WHERE patient = '{}'
    '''.format(session['username']))
    print(session['username'])
    diary_id = cur.fetchone()['id']
    print(diary_id)
    cur.execute('''
        SELECT * FROM diary_entries
        WHERE diary_id = '{}'
    '''.format(diary_id))
    rows = cur.fetchall()

    for row in rows:
        txt = '''
            {} on {}:
            {}
        '''.format(row['author'], row['created'], row['contents'])
        pdf.multi_cell(0,10,txt)

    if os.path.exists("diary/tmp/diary.pdf"):
        os.remove("diary/tmp/diary.pdf")
    pdf.output('diary/tmp/diary.pdf', 'F')

    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(current_app.root_path, 'tmp')
    # Returning file from appended path
    return send_from_directory(uploads, filename)
