import os
from config import db 
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Note

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('admin/home.html')


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    posts = Note.query.all()
    blog_posts = [{'data': post,
                   'note_title': post.name,
                   'note_id': post.id,
                   'note_data': post.data,
                   'note_date': post.date,
                   } 
            for post in posts
    ]
    
    return render_template('admin/settings.html', user=current_user, blog_posts=blog_posts)


## Post management pages
@admin_bp.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    return render_template('admin/posts.html')


# Post adding page
@admin_bp.route('/post-add', methods=['GET', 'POST'])
@login_required
def add_post():
    post_details = None
    if request.method == 'POST': 
        note = request.form.get('post')
        title = request.form.get('post_title')

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id, name=title) 
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('admin.posts'))
    return render_template('admin/post_add.html', user=current_user, post_details=post_details)

