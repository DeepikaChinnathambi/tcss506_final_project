#All route definitions
#!/usr/bin/env python3
from flask import render_template, request, redirect, url_for, session, flash, jsonify, Blueprint,current_app
from app.users import register_user, validate_login,send_reset_email
from app.api import ticketmaster_api
from app.models import Event, UserEvent, User, db
from datetime import datetime
from werkzeug.security import generate_password_hash
from itsdangerous import SignatureExpired, BadSignature,URLSafeTimedSerializer

main = Blueprint('main', __name__) 

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route("/about")
def about():
    return render_template("about.html")

@main.route('/newuser', methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            flash("All fields are required", "danger")
            return render_template('register.html')

        # Server-side password checks
        if len(password) < 8 or not any(c.islower() for c in password) \
        or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password) \
        or not any(c in "!@#$%^&*()-_+=<>?/.,:;{}[]" for c in password):
            flash("Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.", 'danger')
            return redirect(url_for('main.register'))

        # Confirm password match
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            # return render_template('register.html')
            return redirect(url_for('main.register'))

        success, message = register_user(username, email, password)
        if success:
            flash(message, 'success')
            return redirect(url_for('main.login'))
        else:
            flash(message, 'danger')
            return render_template('register.html')

    return render_template('register.html')    

@main.route('/loginvalidate', methods=['GET', 'POST'])
def loginvalidate():
    if request.method == 'POST':
        identifier = request.form.get('useridentifier')# username or email
        password = request.form.get('password')

    
        user, message = validate_login(identifier, password)
        
        if user:
            session['username'] = user.username  
            session['user_id'] = user.id
            flash(message, 'success')
            return redirect(url_for('main.index'))
        else:
            flash(message, 'danger')
            return redirect(url_for('main.login'))

    return render_template('login.html')

@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            # email a secure token
            send_reset_email(user)
            flash("Reset link sent to your email (feature simulated).", "info")
            # # For now, redirect to manual reset
            # return redirect(url_for('main.reset_password', user_id=user.id))
        else:
            flash("Email not found", "danger")
            return redirect(url_for('main.forgot_password'))

    return render_template('forgot_password.html')

@main.route('/reset-password/<int:user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if not all([password, confirm]):
            flash("All fields are required", "danger")
            return redirect(request.url)

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect(request.url)

        if len(password) < 8 or not any(c.islower() for c in password) \
        or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password) \
        or not any(c in "!@#$%^&*()-_+=<>?/.,:;{}[]" for c in password):
            flash("Password must meet security rules.", 'danger')
            return redirect(request.url)

        user.password_hash = generate_password_hash(password)
        db.session.commit()
        flash("Password reset successful. Please log in.", "success")
        return redirect(url_for('main.login'))

    return render_template('reset_password.html', user=user)

@main.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # 1 hour expiry
    except (SignatureExpired, BadSignature):
        flash('The reset link is invalid or expired.', 'danger')
        return redirect(url_for('main.forgot_password'))

    user = User.query.filter_by(email=email).first_or_404()

    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if not all([password, confirm]):
            flash("All fields are required", "danger")
            return redirect(request.url)

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect(request.url)

        if len(password) < 8 or not any(c.islower() for c in password) \
        or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password) \
        or not any(c in "!@#$%^&*()-_+=<>?/.,:;{}[]" for c in password):
            flash("Password must meet security rules.", 'danger')
            return redirect(request.url)

        user.password_hash = generate_password_hash(password)
        db.session.commit()
        flash("Password reset successful. Please log in.", "success")
        return redirect(url_for('main.login'))

    return render_template('reset_password.html', user=user)

@main.route('/profile')
def profile():
    if 'username' not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for('main.login'))
    
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        flash("User not found. Please register.", "danger")
        return redirect(url_for('main.register'))
    
    return render_template('profile.html', user=user)


@main.route('/events/search')
def search_events():
    keyword = request.args.get('keyword')
    city = request.args.get('city')
    state = request.args.get('state')

    try:
        # Convert string dates to datetime if provided
        start_date = None
        end_date = None
        if request.args.get('start_date'):
            start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        if request.args.get('end_date'):
            end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')

        # Get events from Ticketmaster API
        events_data = ticketmaster_api.search_events(
            keyword=keyword,
            city=city,
            state=state,
            start_date=start_date,
            end_date=end_date
        )

        # Process and save events to database
        events = []
        if '_embedded' in events_data and 'events' in events_data['_embedded']:
            for event_data in events_data['_embedded']['events']:
                event = ticketmaster_api.save_event_to_db(event_data)
                events.append(event)

        return render_template('events/search.html', events=events)

    except Exception as e:
        flash(f'Error searching events: {str(e)}', 'error')
        return render_template('events/search.html', events=[])


@main.route('/events/<event_id>')
def event_details(event_id):
    try:
        # First try to get from database
        event = Event.query.filter_by(event_id=event_id).first()

        # If not in database, fetch from API and save
        if not event:
            event_data = ticketmaster_api.get_event_details(event_id)
            event = ticketmaster_api.save_event_to_db(event_data)

        return render_template('events/details.html', event=event)

    except Exception as e:
        flash(f'Error getting event details: {str(e)}', 'error')
        return redirect(url_for('main.search_events'))


@main.route('/events/<event_id>/favorite', methods=['POST'])
def toggle_favorite(event_id):
    if 'username' not in session:
        return jsonify({'error': 'Please login first'}), 401

    try:
        event = Event.query.filter_by(event_id=event_id).first()
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        user_event = UserEvent.query.filter_by(
            user_id=session['user_id'],
            event_id=event.id
        ).first()

        if user_event:
            db.session.delete(user_event)
            message = 'Event removed from favorites'
        else:
            user_event = UserEvent(
                user_id=session['user_id'],
                event_id=event.id,
                status='interested'
            )
            db.session.add(user_event)
            message = 'Event added to favorites'

        db.session.commit()
        return jsonify({'message': message})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/favorites')
def favorite_events():
    if 'username' not in session:
        flash('Please login to view your favorite events', 'warning')
        return redirect(url_for('main.login'))

    try:
        user_events = UserEvent.query.filter_by(user_id=session['user_id']).all()
        events = [ue.event for ue in user_events]
        return render_template('events/favorites.html', events=events)

    except Exception as e:
        flash(f'Error getting favorite events: {str(e)}', 'error')
        return redirect(url_for('main.index'))



            





















