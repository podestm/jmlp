from flask import Blueprint, render_template
from models import Note, Event

# Create the public blueprint
public_bp = Blueprint('public', __name__, template_folder='templates/public')

# Public routes
@public_bp.route('/')
def index():
    return render_template('index.html')


@public_bp.route('/about',  methods=['GET','POST'])
def about():

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

    posts = Note.query.all()
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

    return render_template('public/about.html', event_list=events, blog_posts=blog_posts, cards=cards)
