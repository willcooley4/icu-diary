import os
from flask import Flask, session

from diary.newentry import entry_page

from diary.db import init_db

# init_db()

def create_app(test_config=None):

    # create and configure the app
    # NOTE: if running locally, replace DATABASE= must be the string ending in icu_diary
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
	DATABASE="postgres://alyuctkwauihmb:8424f30704bd4773e151842d1fc846be14327c70e098979e92f6ad4fb8b6b6a5@ec2-34-205-14-168.compute-1.amazonaws.com:5432/d68vsu4crjnc9n",
    # DATABASE="postgres://postgres:password@127.0.0.1:5432/icu_diary",

    )

    with app.app_context():
    	init_db()
    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from diary import db
    db.init_app(app)

    # use blueprint for authorization pages
    from diary import auth
    app.register_blueprint(auth.bp)

    from diary import home
    app.register_blueprint(home.bp)


    from diary import newentry
    app.register_blueprint(newentry.bp)

    from diary import newdiary
    app.register_blueprint(newdiary.bp)

    from diary import invite
    app.register_blueprint(invite.bp)

    from diary import diarysharing
    app.register_blueprint(diarysharing.bp)

    from diary import viewdiary
    app.register_blueprint(viewdiary.bp)

    return app
