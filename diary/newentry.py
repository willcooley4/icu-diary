from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db
from werkzeug.wrappers import request
import diary

bp = Blueprint('entry_page', __name__)  # NOTE: url_prefix?


# allows user to make a new diary submission
# diary entry page for doctor and contributors
# allows for standard, templated, or media submissions
@bp.route('/<diary_id_slug>/entry_page/', methods = 'POST')
def entry_page(diary_id_slug):
    # access form data

    title = request.form.get('title')
    content = request.form.get('content')
    media = request.form.get('media')
    author = flask.session["username"]

    # access database and submit diary entry

    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO diary_entries
        (id, title, created, contents, media, author, diary_id)
        VALUES('{}', '{}', '{}', '{}', '{}')
    '''.format(title, content, media, author, diary_id_slug))
    conn.commit()


    return render_template('newentry.html')

