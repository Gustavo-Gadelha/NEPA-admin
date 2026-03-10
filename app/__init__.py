from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config")

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    from app.extensions import admin, db, login_manager, ph
    from app.views import SecureAdminIndexView

    db.init_app(app)
    ph.init_app(app)
    login_manager.init_app(app)

    admin.init_app(app, index_view=SecureAdminIndexView())

    from app.models import Aluno, AlunoProjeto, Edital, Professor, Projeto
    from app.views import AlunoAdmin, AlunoProjetoAdmin, EditalAdmin, ProfessorAdmin, ProjetoAdmin

    admin.add_view(AlunoAdmin(Aluno, db.session))
    admin.add_view(AlunoProjetoAdmin(AlunoProjeto, db.session))
    admin.add_view(EditalAdmin(Edital, db.session))
    admin.add_view(ProfessorAdmin(Professor, db.session))
    admin.add_view(ProjetoAdmin(Projeto, db.session))

    from app.models import Admin
    from app.routes import bp

    app.register_blueprint(bp)

    from app.commands import register_commands

    register_commands(app)

    return app
