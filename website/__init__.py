from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'PLEASE GIVE ME THAT JOB'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/users.db'
    db.init_app(app)

    from website.views.auth import auth_bp
    from website.views.user import user_bp
    from website.views.misc import misc_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(misc_bp)

    from .models import User, Transaction

    with app.app_context():
        if not path.exists('website/instance/users.db'):
            db.create_all()
            from .fill_db import populate_database
            populate_database()

    return app
