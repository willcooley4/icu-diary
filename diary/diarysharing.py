from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db
import diary
import flask

bp = Blueprint('diary_sharing', __name__)  # NOTE: url_prefix?


# allows nurse to make a new diary for patient
# input patient name, diary name, and emergency contact email
@bp.route('/diary_sharing/', methods = ["POST", "GET"])
def diary_sharing():
    if 'username' not in session:
        return redirect('/auth/login')
    return render_template('diarysharing.html')