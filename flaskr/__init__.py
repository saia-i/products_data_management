
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_apscheduler import APScheduler




login_manager=LoginManager()
login_manager.login_view="app.login"
login_manager.login_message="Please login"

db=SQLAlchemy()
migrate=Migrate()
scheduler = APScheduler()

class Config:
    SCHEDULER_API_ENABLED = True


def create_app():
    app=Flask(__name__)
    app.config["SECRET_KEY"]="b'_\xd2\x0c\x0b\xeb\xeb@6\xe1\xc7rP\xb7\x9dP\x96'"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/mercari' 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
    from flaskr.views import bp
    app.register_blueprint(bp)
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    
    return app

