import psycopg2
import psycopg2.extras

import click
from flask import current_app, g
from flask.cli import with_appcontext
import uuid
import hashlib


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

    # with db.cursor() as cursor:
    #     cursor.execute(current_app.open_resource('test_diary.sql').read())

    # with current_app.open_resource('schema.sql') as f:
    #     db.execute(f.read().decode('utf8'))

    with db.cursor() as cursor:
        cursor.execute(current_app.open_resource('schema.sql').read())

    # Create admin account

    salt = uuid.uuid4().hex
    hash_obj = hashlib.new('sha512')
    password_salted = salt + 'admin'  # TODO: Create secure password for administrator
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join(['sha512', salt, password_hash])

    # Create user account
    db.cursor().execute('''
        INSERT INTO users(username, full_name, password, profile_pic, user_type, email)
        VALUES ('admin', 'System Administrator', '{}', '{}', 'admin', 'admin@icu.com')
    '''.format(password_db_string, 'lala.jpg'))
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

