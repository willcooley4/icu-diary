import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE="postgres://postgres:password@127.0.0.1:5432/icu_diary"
        # DATABASE=os.path.join(app.instance_path, 'diary.'),
    )
    

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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    # home page for all users
    # shows linked pages the user has access to
    @app.route('/')
    def home():
        #todo
        return ''

    # diary entry page for doctor and contributors
    # allows for standard, templated, or media submissions
    @app.route('/entry_page')
    def entry_page():
        #todo
        return ''

    # diary viewing page for patient
    # scrollable page for diary entries, allows for pdf download
    @app.route('/diary_vieiwing')
    def diary_viewing():
        #todo
        return ''

    # diary sharing page for contributors
    # allows user to share diary with outside user via email, text, social media
    @app.route('/diary_sharing')
    def diary_sharing():
        #todo
        return ''
    
    # signup approval page for primary contributor 
    # allows user to see who has requested access to diary and accept/decline join requests
    @app.route('/signup_approval')
    def signup_approval():
        #todo
        return ''

    # diary creation page that allows doctor to create new patient diary
    @app.route('/create_diary')
    def create_diary():
        #todo
        return ''
    

    return app