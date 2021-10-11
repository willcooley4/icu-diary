from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from diary.db import get_db
import diary
import flask

bp = Blueprint('entry_page', __name__)  # NOTE: url_prefix?


# allows user to make a new diary submission
# diary entry page for doctor and contributors
# allows for standard, templated, or media submissions
@bp.route('/entry_page/', methods = ["POST", "GET"])
def entry_page():
    # access form data
    if 'username' not in session:
        return redirect('/auth/login')
    
    context = {'e': 0, 'message': ''}

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        media = request.form.get('media')
        author = flask.session["username"]
        # access database and submit diary entry

        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO diary_entries
            (title, contents, media, author, diary_id)
            VALUES('{}', '{}', '{}', '{}', '{}')
        '''.format(title, content, media, author, 1))
        conn.commit()
        context = {'e': 1, 'message': 'Message submitted!'}
        return render_template('newentry.html', **context)


    return render_template('newentry.html', **context)

