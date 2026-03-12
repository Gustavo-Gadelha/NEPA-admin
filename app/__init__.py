from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def _load_admin():
    from flask import current_app

    from app.extensions import db
    from app.models import Admin

    name_ = current_app.config["ADMIN_NAME"]
    email_ = current_app.config["ADMIN_EMAIL"]
    password_ = current_app.config["ADMIN_PASSWORD"]
    role_ = current_app.config["ADMIN_ROLE"]

    existing = db.session.execute(db.select(Admin).where(Admin.email == email_)).scalar()

    if not existing:
        admin = Admin(nome=name_, email=email_, password=password_, permissao=role_)
        db.session.add(admin)
        db.session.commit()
        current_app.logger.info(f"Admin {email_} created successfully.")


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config")

    from app.extensions import admin, babel, db, login_manager, ph
    from app.views import SecureAdminIndexView

    db.init_app(app)
    ph.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    admin.init_app(app, index_view=SecureAdminIndexView())

    from app.models import Admin, Aluno, AlunoProjeto, Edital, Professor, Projeto
    from app.views import AlunoAdmin, AlunoProjetoAdmin, EditalAdmin, ProfessorAdmin, ProjetoAdmin

    admin.add_view(AlunoAdmin(Aluno, db.session, name="Alunos", category="Usuários"))
    admin.add_view(ProfessorAdmin(Professor, db.session, name="Professores", category="Usuários"))
    admin.add_view(ProjetoAdmin(Projeto, db.session, name="Projetos", category="Projetos"))
    admin.add_view(AlunoProjetoAdmin(AlunoProjeto, db.session, name="Inscrições", category="Projetos"))
    admin.add_view(EditalAdmin(Edital, db.session, name="Editais", category="Editais"))

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Admin, user_id)

    from app.commands import register_commands

    register_commands(app)

    from app.exceptions import register_error_handlers

    register_error_handlers(app)

    with app.app_context():
        if app.config["TESTING"]:
            db.create_all()

        _load_admin()

    return app
