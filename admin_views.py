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



@admin_bp.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    posts = Notes.query.all()
    blog_posts = [{'data': post,
                   'note_title': post.name,
                   'note_id': post.id,
                   'note_data': post.data,
                   'note_date': post.date,
                   } 
            for post in posts
    ]
    return render_template('admin/posts.html', user=current_user, blog_posts=blog_posts)


# Post adding page
@admin_bp.route('/post-add', methods=['GET', 'POST'])
@login_required
def add_post():
    return render_template('admin/post_add.html')

