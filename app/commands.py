import click

from app.extensions import db, ph
from app.models import Admin


def register_commands(app):
    @app.cli.command("create-admin")
    @click.option("--name", prompt=True, help="Admin name")
    @click.option("--email", prompt=True, help="Admin email")
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Admin password")
    @click.option("--role", default="admin", show_default=True, help="User permission")
    def create_admin(email, name, password, role):
        existing = Admin.query.filter_by(email=email).first()

        if existing:
            click.echo("An admin with this email already exists.")
            return

        admin = Admin(
            nome=name,
            email=email,
            password=ph.generate_password_hash(password),
            permissao=role,
        )

        db.session.add(admin)
        db.session.commit()

        click.echo(f"Admin {email} created successfully.")
