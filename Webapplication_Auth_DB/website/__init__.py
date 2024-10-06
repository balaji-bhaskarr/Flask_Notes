from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_Name = 'database.db'
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hfghfbdga bhdkr sawkeu'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}'

    db.init_app(app=app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager.login_view = 'auth.login' # specifies what method should be called when there's no login
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_database(app):
    if not os.path.exists('website/'+DB_Name):
        with app.app_context():
            db.create_all()
            print('Database created!')
        
    