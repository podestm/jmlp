import os
from config import db 
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import inspect, update
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

### POSTS MANAGEMENT ###

#Posts overview page
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
    post_details = None
    if request.method == 'POST': 
        note = request.form.get('post')
        title = request.form.get('post_title')

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Notes(data=note, name=title) 
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('admin.posts'))
    return render_template('admin/post_add.html', user=current_user, post_details=post_details)


# Post editing page - basically same template as for adding but prefilled and used update function from SQL Alchemy 
@admin_bp.route('/post-edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Notes.query.filter(Notes.id == post_id).first_or_404()
    post_details = {
        'id': post.id,
        'name': post.name,
        'date': post.date,
        'data': post.data,
        }
    
    if request.method == 'POST': 
        post_data = request.form.get('post')
        post_title = request.form.get('post_title')

        if len(post_data) < 1:
            flash('Note is too short!', category='error') 
        else:
            update_post = (
                update(Notes).where(Notes.id == post_id)
                .values(name = post_title, data = post_data)
            )
            db.session.execute(update_post)
            db.session.commit()
            
            return redirect(url_for('admin.posts'))
    return render_template('admin/post_add.html', user=current_user, post_details=post_details)


# Post delete function
@admin_bp.route('/delete-post/<int:post_id>', methods=['GET','POST'])
@login_required
def delete_post(post_id):  
    note = Notes.query.get(post_id)
    if note:
        db.session.delete(note)
        db.session.commit()

    return redirect(url_for('admin.posts'))

### EVENT MANAGEMENT ###
