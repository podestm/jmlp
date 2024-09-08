from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import User  # Ensure you import your models

# Create the auth blueprint
auth_bp = Blueprint('auth', __name__)

# Login route
@auth_bp.route('/login/', methods=["GET", "POST"])
def login():
    error = False
    if request.method == "POST":
        # Get the user by username
        user = User.query.filter_by(username=request.form["username"]).first()

        if user is None:
            print("User not found")  # Debugging output
            error = True
        elif not check_password_hash(user.password_hash, request.form["password"]):
            print("Password does not match")  # Debugging output
            error = True
        else:
            # Log in the user
            login_user(user)
            print(f"Logged in as: {current_user.username}")  # Debugging output

            # Redirect to the next page or dashboard
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))

    # If the login fails, stay on the login page
    return render_template("auth/login_page.html", error=error)

# Logout route
@auth_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))  # Redirect to index after logout