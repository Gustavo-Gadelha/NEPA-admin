from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app.extensions import ph
from app.models import Admin

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        admin = Admin.query.filter_by(email=email).first()

        if not admin or not ph.check_password_hash(admin.password, password):
            flash("Email ou senha inválidos.", "error")
            return redirect(url_for("auth.login"))

        login_user(admin)
        flash("Login realizado com sucesso.", "success")

        return redirect("/admin")

    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
