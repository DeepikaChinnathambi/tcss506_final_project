# users.py
from flask import current_app,url_for
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from app import mail
from itsdangerous import URLSafeTimedSerializer

def register_user(username,email, password):
    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return False, "Username already exists"

    if User.query.filter_by(email=email).first():
        return False, "Email already registered"

    # Hash the password
    hashed = generate_password_hash(password)

    # Create and add user to DB
    user = User(username=username, email=email, password_hash=hashed)
    db.session.add(user)
    db.session.commit()
    
    return True, "User registered successfully"

def validate_login(identifier, password):
    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    if user and check_password_hash(user.password_hash, password):
        return user, "Login successful"
    return False, "Invalid username/email or password"

def get_all_users():
    return User.query.all

def send_reset_email(user):
    # Generate token
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(user.email, salt='password-reset-salt')

    # Generate URL
    reset_url = url_for('main.reset_password_token', token=token, _external=True)

    # Create and send message
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, click the following link:
{reset_url}

If you did not request this, please ignore this email.
'''
    mail.send(msg)