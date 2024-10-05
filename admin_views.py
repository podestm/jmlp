from flask import Blueprint, render_template
from flask_login import login_required
from models import Note

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('admin/home.html')


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/settings')
@login_required
def settings():
    return render_template('admin/settings.html')


## Post management pages
@admin_bp.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    return render_template('admin/posts.html')

