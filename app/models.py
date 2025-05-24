#Database models(User,Event,Rsvp,etc.)
#Create Models (Database Schema)

from datetime import datetime, timezone
from . import db # Import the db object from __init__.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)# Store hashed password
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    favorite_events = db.relationship('Event', secondary='user_event', backref='favorited_by')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(100), unique=True, nullable=False)  # Ticketmaster event ID
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    venue_name = db.Column(db.String(200))
    venue_city = db.Column(db.String(100))
    venue_state = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    ticket_url = db.Column(db.String(500))
    price_range = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class UserEvent(db.Model):
    __tablename__ = 'user_event'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    status = db.Column(db.String(20), default='interested')  # interested, going, not_interested
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    #can later add models like Event, RSVP, etc., but started with User.