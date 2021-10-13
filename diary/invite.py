from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db


bp = Blueprint('invite', __name__)  # NOTE: url_prefix?

@bp.route('/invite', methods=('GET', 'POST'))
def invite():
    if 'username' not in session:
        return redirect('/auth/login')
    return render_template('invite.html')