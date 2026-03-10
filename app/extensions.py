from flask_admin import Admin
from flask_argon2 import Argon2
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
admin = Admin()
ph = Argon2()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    from app.models import Admin

    return Admin.query.get(user_id)
