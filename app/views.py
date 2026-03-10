from flask import redirect, request, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_login import current_user


class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.permissao == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))


class SecureModelView(ModelView):
    form_base_class = SecureForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.permissao == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login", next=request.url))

    def on_model_change(self, form, model, is_created):
        from app.extensions import ph

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

    column_exclude_list = ("password",)

    column_searchable_list = ("nome", "matricula", "email")
    column_filters = ("curso", "permissao", "data_ingresso")

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

    column_exclude_list = ("password",)

    column_filters = ("curso", "aprovado")
    column_searchable_list = ("nome", "matricula", "email")

    form_excluded_columns = ("projetos_propostos",)


class ProjetoAdmin(SecureModelView):
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

    column_filters = (
        "curso",
        "situacao",
        "aprovado",
        "data_criacao",
    )

    column_searchable_list = ("titulo", "linhaDePesquisa")

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

    column_searchable_list = (
        "aluno.nome",
        "projeto.titulo",
    )


class EditalAdmin(SecureModelView):
    column_list = (
        "id",
        "nome",
        "slug",
        "admin",
        "data_criacao",
    )

    column_searchable_list = ("nome", "slug")

    column_filters = ("data_criacao",)
