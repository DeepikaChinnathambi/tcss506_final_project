#Database models(User,Event,Rsvp,etc.)
#Create Models (Database Schema)
from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)# Store hashed password
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #can later add models like Event, RSVP, etc., but start with User.