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
        events = Event.query.order_by(Event.Event_date).all()

        cards = [{'data': event,
                'event_id': event.IdEvent,
                'show_button': event.Event_opened == 1,
                'event_name': event.Event_name,
                'event_date': event.Event_date.strftime("%d.%m.%Y"),
                'event_organizator': event.Event_organizator,
                'event_badge': event.Event_badge,
                'event_place': event.Event_place,
                'event_closed': event.Event_opened == 0,
                'event_opened': event.Event_opened == 1,
                'propositions_file': event.Propositions_file_name,
                'results_file': event.Results_file_name
                }
            for event in events
        ]

        posts = Notes.query.all()
        blog_posts = [{'data': post,
                    'note_title': post.name,
                    'note_id': post.id,
                    'note_data': post.data,
                    'note_date': post.date,
                    'note_type': post.Note_type,
                    'note_image': post.Note_image_url != None,
                    'image_url': post.Note_image_url
                    }
                for post in posts
        ]

        return render_template('public/home.html', event_list=events, blog_posts=blog_posts, cards=cards)



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
            new_note = Notes(data=note, user_id=current_user.id, name=title) 
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('admin.posts'))
    return render_template('admin/post_add.html', user=current_user, post_details=post_details)

