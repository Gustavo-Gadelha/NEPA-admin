from flask import redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_login import current_user, login_user, logout_user

from app.extensions import ph
from app.forms import LoginForm


class SecureAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for(".login_view"))
        return super().index()

    @expose("/login/", methods=("GET", "POST"))
    def login_view(self):
        if current_user.is_authenticated:
            return redirect(url_for(".index"))

        form = LoginForm(request.form)
        if form.validate_on_submit():
            login_user(form.user)

            if "next" in request.args:
                next_url = request.args.get("next")
                if next_url:
                    return redirect(next_url)

            return redirect(url_for(".index"))

        self._template_args["form"] = form
        return super().index()

    @expose("/logout/")
    def logout_view(self):
        logout_user()
        return redirect(url_for(".index"))


class SecureModelView(ModelView):
    form_base_class = SecureForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.permissao.lower() == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.login_view", next=request.url))

    def on_model_change(self, form, model, is_created):
        if hasattr(model, "password") and form.password.data:
            model.password = ph.generate_password_hash(form.password.data)


class AlunoAdmin(SecureModelView):
    column_list = (
        "id",
        "nome",
        "matricula",
        "curso",
        "email",
        "telefone",
        "data_ingresso",
        "permissao",
    )

    column_filters = ("curso", "permissao", "data_ingresso")
    column_searchable_list = ("nome", "matricula", "email")
    column_exclude_list = ("password",)

    form_excluded_columns = ("projetos",)


class ProfessorAdmin(SecureModelView):
    column_list = (
        "id",
        "nome",
        "matricula",
        "curso",
        "email",
        "telefone",
        "aprovado",
        "permissao",
    )

    column_filters = ("curso", "permissao", "aprovado")
    column_searchable_list = ("nome", "matricula", "email")
    column_exclude_list = ("password",)

    form_excluded_columns = ("projetos_propostos",)


class ProjetoAdmin(SecureModelView):
    column_labels = {
        "linhaDePesquisa": "Linha de Pesquisa",
        "palavrasChave": "Palavras Chave",
        "objetivoGeral": "Objetivo Geral",
        "objetivoEspecifico": "Objetivo Especifico",
        "cronogramaDeAtividade": "Cronograma de Atividade",
    }

    column_list = (
        "id",
        "titulo",
        "professor",
        "curso",
        "vagas",
        "vagas_ocupadas",
        "situacao",
        "aprovado",
        "data_criacao",
    )

    column_filters = ("curso", "situacao", "aprovado", "data_criacao")
    column_searchable_list = ("titulo", "id")

    form_excluded_columns = ("alunos_cadastrados",)


class AlunoProjetoAdmin(SecureModelView):
    column_list = (
        "id",
        "aluno",
        "projeto",
        "aprovado",
        "reprovado",
    )

    column_filters = ("aprovado", "reprovado")
    column_searchable_list = ("aluno.nome", "aluno.email", "projeto.titulo", "projeto.id")


class EditalAdmin(SecureModelView):
    # TODO: Implementar salvamento de arquivo para permitir criação
    can_create = False

    column_labels = {
        "Arquivo Pdf": "Caminho do arquivo",
    }

    column_list = (
        "id",
        "nome",
        "slug",
        "admin",
        "arquivo_pdf",
        "data_criacao",
    )

    column_filters = ("data_criacao",)
    column_searchable_list = ("nome", "slug")

    form_excluded_columns = ("slug",)

    def on_model_change(self, form, model, is_created):
        if not model.slug:
            model.generate_slug()
