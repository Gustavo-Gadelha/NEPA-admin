from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config")

    from app.extensions import admin, babel, db, login_manager, ph
    from app.views import SecureAdminIndexView

    db.init_app(app)
    babel.init_app(app)
    admin.init_app(app, index_view=SecureAdminIndexView())
    ph.init_app(app)
    login_manager.init_app(app)

    from app.models import Admin, Aluno, AlunoProjeto, Edital, Professor, Projeto
    from app.views import AlunoAdmin, AlunoProjetoAdmin, EditalAdmin, ProfessorAdmin, ProjetoAdmin

    admin.add_view(AlunoAdmin(Aluno, db.session))
    admin.add_view(AlunoProjetoAdmin(AlunoProjeto, db.session))
    admin.add_view(EditalAdmin(Edital, db.session))
    admin.add_view(ProfessorAdmin(Professor, db.session))
    admin.add_view(ProjetoAdmin(Projeto, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Admin, user_id)

    from app.commands import register_commands

    register_commands(app)

    from app.exceptions import register_error_handlers

    register_error_handlers(app)

    return app
