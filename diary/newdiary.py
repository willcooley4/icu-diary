from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db
import diary
import flask

bp = Blueprint('new_diary', __name__)  # NOTE: url_prefix?


# allows nurse to make a new diary for patient
# input patient name, diary name, and emergency contact email
@bp.route('/new_diary/', methods = ["POST", "GET"])
def new_diary():
    if 'username' not in session:
        return redirect('/auth/login')

    context = {'e': 0, 'message': ''}

    if request.method == 'POST':
        context = {'e': 1, 'message': 'Diary Created'}
        return render_template('newdiary.hmtl', **context)
        
    return render_template('newdiary.html', **context)
