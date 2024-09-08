from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models import User  # Ensure you import your models

# Create the auth blueprint
auth_bp = Blueprint('auth', __name__)

# Login route
@auth_bp.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login_page.html", error=False)

    user = User.query.filter_by(username=request.form["username"]).first()

    if user is None:
        return render_template("auth/login_page.html", error=True)

    if not check_password_hash(user.password_hash, request.form["password"]):
        return render_template("auth/login_page.html", error=True)

    # Log in the user after successful authentication
    login_user(user)

    return redirect(url_for('public.index'))


# Logout route
@auth_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))  # Redirect to index after logout