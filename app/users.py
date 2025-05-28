# users.py
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash

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

