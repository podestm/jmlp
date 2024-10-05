import os
from config import db 
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Notes, Event

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('admin/home.html')


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
        return render_template('admin/settings.html')



@admin_bp.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
        return render_template('admin/blog.html')


# Post adding page
@admin_bp.route('/post-add', methods=['GET', 'POST'])
@login_required
def add_post():
    return render_template('admin/post_add.html')

