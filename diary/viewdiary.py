from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db
import diary
import flask


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
        SELECT * FROM diary_entries
    ''')
    rows = cur.fetchall()

    context = {'entries': rows}
    return render_template('viewdiary.html', **context)
