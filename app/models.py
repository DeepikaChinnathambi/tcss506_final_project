from datetime import datetime, timezone
from . import db  # Import the db object from __init__.py


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar_url = db.Column(db.String(500), default='images/avatar.png')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relationship to UserEvent (association table)
    event_links = db.relationship('UserEvent', back_populates='user', lazy='dynamic')

    @property
    def favorites(self):
        return [link.event for link in self.event_links.all() if link.is_favorite]

    @property
    def rsvps(self):
        return [link.event for link in self.event_links.all() if link.rsvp_status == 'going']


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(100), unique=True, nullable=False)
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

    # Relationship to UserEvent (association table)
    event_links = db.relationship('UserEvent', back_populates='event', lazy='dynamic')

    @property
    def rsvp_users(self):
        # Return all users who have RSVP'd "going" for this event
        return [link.user for link in self.event_links.filter_by(rsvp_status='going').all()]


class UserEvent(db.Model):
    __tablename__ = 'user_event'
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    
    is_favorite = db.Column(db.Boolean, default=False)
    rsvp_status = db.Column(db.String(20), default='interested')  # going, interested, not_interested
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Bidirectional relationships
    user = db.relationship('User', back_populates='event_links')
    event = db.relationship('Event', back_populates='event_links')

    def __repr__(self):
        return f'<UserEvent user={self.user_id} event={self.event_id} fav={self.is_favorite} rsvp={self.rsvp_status}>'
