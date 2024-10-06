from flask import Blueprint, render_template, request
from flask_login import current_user
from sqlalchemy import or_
import db
from models import Notes, Event, Racer, Team, EventHasRacer

# Create the public blueprint
public_bp = Blueprint('public', __name__, template_folder='templates/public')

# Public routes
@public_bp.route('/')
def index():
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
    
    
    return render_template('public/index.html', blog_posts=blog_posts)


@public_bp.route('/events', methods=['GET','POST'])
def events():
    
    return render_template('public/events.html')


@public_bp.route('/blank',  methods=['GET','POST'])
def home():

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