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
    return render_template('public/events.html', event_list=events, cards=cards)


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



@public_bp.route('/registration/<int:event_id>', methods=['GET','POST'])
def register(event_id):
    
    event = Event.query.filter(Event.IdEvent == event_id).first_or_404()
    event_details = {
        'id': event.IdEvent,
        'name': event.Event_name,
        'date': event.Event_date.strftime("%d.%m.%Y"),
        'badge': event.Event_badge,
        'place': event.Event_place,
        'closed': event.Event_opened == 0,
        'opened': event.Event_opened == 1,
        'propositions_name': event.Propositions_file_name,
        'results_name': event.Results_file_name
    }
    
    racers = Racer.query.with_entities(Racer.Racer_firstName, Racer.Racer_lastName, Racer.Racer_birthYear, Racer.Racer_teamName, Racer.Racer_gender).all()
    racer_list = [
    {
        'firstName': racer.Racer_firstName,
        'lastName': racer.Racer_lastName,
        'birthYear': racer.Racer_birthYear,
        'teamName': racer.Racer_teamName,
        'gender': racer.Racer_gender
    }   
        for racer in racers
    ]
    
    teams = Team.query.with_entities(Team.Team_name).all()
    
    if request.method == 'POST':
        racer_firstName = request.form.get('racer_firstName')
        racer_lastName = request.form.get('racer_lastName')
        racer_birthYear = request.form.get('racer_birthYear')
        racer_gender = request.form.get('racer_gender')
        racer_teamName = request.form.get('racer_teamName')
        racer_email = request.form.get('racer_email')
        racer_newTeam = request.form.get('racer_newTeam')
    
        check_racer = Racer.query.filter(
            Racer.Racer_firstName == racer_firstName,
            Racer.Racer_lastName == racer_lastName,
            Racer.Racer_birthYear == racer_birthYear,
        ).with_entities(Racer.IdRacer, Racer.Racer_teamName).first()

        if check_racer is None:
            
            if racer_teamName == 'AddNewTeam':
                racer_team = racer_newTeam
                new_team = Team(Team_name=racer_team)
                db.session.add(new_team)
                db.session.commit()
            else:
                racer_team = racer_teamName
                
            new_racer = Racer(
                Racer_firstName=racer_firstName,
                Racer_lastName=racer_lastName,
                Racer_birthYear=racer_birthYear,
                Racer_teamName=racer_team,
                Racer_gender=racer_gender,
                Racer_email = racer_email
            )
            db.session.add(new_racer)
            db.session.commit()
         
        elif not check_racer[1] == racer_teamName:
            if racer_teamName == 'AddNewTeam':
                racer_team = racer_newTeam
                new_team = Team(Team_name=racer_team)
                db.session.add(new_team)
                db.session.commit()
                update_values = {'Racer_teamName': racer_team, 'Racer_email': racer_email}
            else:
                update_values = {'Racer_teamName': racer_teamName, 'Racer_email': racer_email}

            db.session.query(Racer).filter(Racer.IdRacer == check_racer[0]).update(update_values)
            db.session.commit()

            
        existing_racer = Racer.query.filter(
            Racer.Racer_firstName == racer_firstName,
            Racer.Racer_lastName == racer_lastName,
            Racer.Racer_birthYear == racer_birthYear,
            or_(Racer.Racer_teamName == racer_teamName,Racer.Racer_teamName == racer_newTeam)).first()
        
        matching_event = Event.query.filter(Event.IdEvent == event_id).first()

        if existing_racer and matching_event:
            new_registration = EventHasRacer(EventId=matching_event.IdEvent, RacerId=existing_racer.IdRacer)
            db.session.add(new_registration)
            db.session.commit()
        
    return render_template('public/registration.html',user=current_user, racers=racers, teams=teams, racer_list=racer_list, event_details=event_details)

