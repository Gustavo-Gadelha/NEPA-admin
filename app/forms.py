from flask_wtf import FlaskForm
from wtforms import fields, validators

from app.extensions import db, ph
from app.models import Admin


class LoginForm(FlaskForm):
    email = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    user = None

    def validate_email(self, field):
        self.user = db.session.execute(db.select(Admin).where(Admin.email == field.data)).scalar()
        if self.user is None:
            raise validators.ValidationError("Email inválido")

    def validate_password(self, field):
        if self.user is None:
            return
        if not ph.check_password_hash(self.user.password, field.data):
            raise validators.ValidationError("Senha inválida")
