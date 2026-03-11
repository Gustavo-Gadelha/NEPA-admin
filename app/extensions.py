from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme
from flask_argon2 import Argon2
from flask_babel import Babel, get_locale
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ph = Argon2()
login_manager = LoginManager()
babel = Babel(locale_selector=get_locale)

admin = Admin(
    theme=Bootstrap4Theme(
        base_template="master.html",
        fluid=True,
    )
)
