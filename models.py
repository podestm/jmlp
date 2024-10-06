from config import db  # Import the db instance from extensions
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)  # Return the user ID as a string

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Prague')))
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    commenter = db.relationship('User', backref='comments')

class Event(db.Model):

    IdEvent = db.Column(db.Integer, primary_key=True)
    Event_name = db.Column(db.String(150))
    Event_date = db.Column(db.Date)
    Event_time = db.Column(db.Time)
    Event_place = db.Column(db.String(150))
    Event_final = db.Column(db.Integer)
    Event_season = db.Column(db.String(10))
    Results_file_name = db.Column(db.String(100))
    Results_file_ext = db.Column(db.String(10))
    Results_file_url = db.Column(db.String(100))
    Propositions_file_name = db.Column(db.String(100))
    Propositions_file_ext = db.Column(db.String(10))
    Propositions_file_url = db.Column(db.String(100))
    Event_organizator = db.Column(db.String(100))
    Event_badge = db.Column(db.String(100))
    Event_opened = db.Column(db.Integer)

class Notes(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/Prague')))
    Note_type = db.Column(db.String(45))
    Note_image_url = db.Column(db.String(255))
    
class Racer(db.Model):
    __tablename__ = "racer"
    
    IdRacer = db.Column(db.Integer, primary_key=True)
    Racer_firstName = db.Column(db.String(100))
    Racer_lastName = db.Column(db.String(100))
    Racer_birthYear = db.Column(db.String(100))
    Racer_gender = db.Column(db.Enum('Muž', 'Žena'))
    Racer_email = db.Column(db.String(100))
    Racer_teamName = db.Column(db.String(100), db.ForeignKey('team.Team_name'))
    
class Team(db.Model):
    __tablename__ = "team"
    
    IdTeam = db.Column(db.Integer, primary_key=True)
    Team_name = db.Column(db.String(100))
    Team_contact = db.Column(db.String(100))
    
class EventHasRacer(db.Model):
    __tablename__ = "eventHasRacer"
    
    EventId = db.Column(db.Integer, db.ForeignKey('event.IdEvent'), primary_key=True)
    RacerId = db.Column(db.Integer, db.ForeignKey('racer.IdRacer'), primary_key=True)
    RegistrationTimestamp = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)