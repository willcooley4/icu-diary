from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db


bp = Blueprint('home', __name__)  # NOTE: url_prefix?

@bp.route('/', methods=('GET', 'POST'))
def home():
    return render_template('index.html')