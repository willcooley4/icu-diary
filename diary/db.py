import psycopg2
import psycopg2.extras

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            current_app.config['DATABASE'],
        )
        g.db.cursor_factory = psycopg2.extras.RealDictCursor  # row factory equivilent 

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.autocommit = True  # NOTE: we may want to eliminate this line if the need arises

    with db.cursor() as cursor:
        cursor.execute(current_app.open_resource('test_diary.sql').read())

    # with current_app.open_resource('schema.sql') as f:
    #     db.execute(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

