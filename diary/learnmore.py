from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import diary
import flask

bp = Blueprint('learn_more', __name__)  # NOTE: url_prefix?


# allows user to make a new diary submission
# diary entry page for doctor and contributors
# allows for standard, templated, or media submissions
@bp.route('/learn_more/', methods = ["POST", "GET"])
def learn_more():
    if 'username' not in session:
        return redirect('/auth/login')
    return render_template('learnmore.html')