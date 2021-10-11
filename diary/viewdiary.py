from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db
import diary
import flask

bp = Blueprint('view_diary', __name__)  # NOTE: url_prefix?

# scroll through diary entries
# posts sorted chronologically
@bp.route('/view_diary/', methods = ["POST", "GET"])
def view_diary():
    return render_template('viewdiary.html')
