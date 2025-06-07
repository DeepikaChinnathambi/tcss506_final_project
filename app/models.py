#Database models(User,Event,Rsvp,etc.)
#Create Models (Database Schema)

from datetime import datetime, timezone
from . import db # Import the db object from __init__.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)# Store hashed password
    avatar_url = db.Column(db.String(500), default='images/default_avatar.png')  # Default avatar path
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    favorite_events = db.relationship('Event', secondary='user_event', backref='favorited_by', lazy='dynamic')

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), default='interested')  # interested, going, not_interested
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    # Add relationships for easier access
    user = db.relationship('User', backref=db.backref('user_events', lazy=True))
    event = db.relationship('Event', backref=db.backref('user_events', lazy=True))

    def __repr__(self):
        return f'<UserEvent {self.user_id}:{self.event_id}>'

    #can later add models like RSVP, etc.,