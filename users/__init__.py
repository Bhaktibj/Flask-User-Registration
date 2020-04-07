import os
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_shorturl import ShortUrl

app = Flask(__name__)

app.config.from_object(os.getenv('USER_APP_SETTINGS'))

login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
db = SQLAlchemy(app)

from .routes import user_app

app.register_blueprint(user_app)
from users.models.models import User


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

