from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///recipes.db'
app.config['SECRET_KEY']='0c70dc8668ffe8b846ace6018a789c9ef30e8458e2cbd3fd'

db = SQLAlchemy(app)
migrate = Migrate(app,db)
admin = Admin()
admin.init_app(app)


login_manager = LoginManager(app)
from myapp.models import User
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from myapp import routes, models