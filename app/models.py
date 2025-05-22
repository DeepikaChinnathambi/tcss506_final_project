#Database models(User,Event,Rsvp,etc.)
#Create Models (Database Schema)

from datetime import datetime
from . import db # Import the db object from __init__.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    #can later add models like Event, RSVP, etc., but started with User.