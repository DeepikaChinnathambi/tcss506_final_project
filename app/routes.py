#All route definitions
#!/usr/bin/env python3
import os
from flask import render_template, request, redirect, url_for, session, flash, jsonify, Blueprint,current_app
from app.users import register_user, validate_login,send_reset_email
from app.api import ticketmaster_api
from app.models import Event, UserEvent, User, db
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from itsdangerous import SignatureExpired, BadSignature,URLSafeTimedSerializer

main = Blueprint('main', __name__) 
# Configure upload settings
UPLOAD_FOLDER = os.path.join('app', 'static', 'images', 'avatars')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            session['avatar_url'] = user.avatar_url
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

@main.route('/update_avatar', methods=['POST'])
def update_avatar():
    if 'username' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('main.login'))

    if 'avatar' not in request.files:
        flash('No file uploaded', 'warning')
        return redirect(url_for('main.profile'))

    file = request.files['avatar']
    
    if file.filename == '':
        flash('No file selected', 'warning')
        return redirect(url_for('main.profile'))

    if file and allowed_file(file.filename):
        # Create upload folder if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Secure the filename and make it unique
        filename = secure_filename(file.filename)
        username = session['username']
        unique_filename = f"{username}_{filename}"
        
        # Save the file
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Update user's avatar_url in database
        user = User.query.filter_by(username=username).first()
        user.avatar_url = f"images/avatars/{unique_filename}"
        db.session.commit()
        
        # Update session with new avatar_url
        session['avatar_url'] = user.avatar_url
        
        flash('Avatar updated successfully!', 'success')
    else:
        flash('Invalid file type. Please use PNG, JPG, JPEG, or GIF.', 'danger')
    
    return redirect(url_for('main.profile'))

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
        
        try:
            user = User.query.filter_by(username=session.get('username')).first()
            favorites = [event.event_id for event in user.favorites if event is not None]
            rsvps = [event.event_id for event in user.rsvps if event is not None]
        except Exception as e:
            favorites = []
            rsvps = []
            

        return render_template('events/search.html', events=events, favorites=favorites, rsvps=rsvps)
        
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
        
        try:
            user = User.query.filter_by(username=session.get('username')).first()
            favorites = [event.event_id for event in user.favorites if event is not None]
            rsvps = [event.event_id for event in user.rsvps if event is not None]
        except Exception as e:
            favorites = []
            rsvps = []

        return render_template('events/details.html', event=event, favorites=favorites, rsvps=rsvps)
        
    except Exception as e:
        flash(f'Error getting event details: {str(e)}', 'error')
        return redirect(url_for('main.search_events'))

@main.route('/events/<event_id>/favorite', methods=['POST'])
def toggle_favorite(event_id):
    if 'username' not in session:
        return jsonify({'error': 'Please login first'}), 401

    if 'user_id' not in session:
        return jsonify({'error': 'Session error. Please login again.'}), 401

    try:
        # First verify the user existsAdd commentMore actions
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found. Please login again.'}), 401

        # Debug logging
        current_app.logger.info(f"Toggle favorite for user {user.username} (ID: {user.id}) and event {event_id}")

        # Find the event
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            current_app.logger.error(f"Event not found with ID: {event_id}")
            return jsonify({'error': 'Event not found'}), 404

        current_app.logger.info(f"Found event: {event.name} (ID: {event.event_id})")

        # Check for existing favorite
        user_event = UserEvent.query.filter_by(
            user_id=session['user_id'],
            event_id=event.id
        ).first()

        try:
            if user_event:
                current_app.logger.info(f"Removing favorite (UserEvent ID: {user_event.event_id})")
                db.session.delete(user_event)
                fave = False
                message = 'Event removed from favorites'
            else:
                current_app.logger.info(f"Adding new favorite for event ID: {event.event_id}")
                user_event = UserEvent(
                    user_id=session['user_id'],
                    event_id=event.id,
                    is_favorite=True,  # Set as favorite
                    rsvp_status='interested'
                )
                fave = True
                db.session.add(user_event)
                message = 'Event added to favorites'

            db.session.commit()
            current_app.logger.info("Successfully committed database changes")
            return jsonify({'message': message, 'status': 'success', 'favorited': fave})
            
        except Exception as db_error:
            db.session.rollback()
            current_app.logger.error(f"Database error in toggle_favorite: {str(db_error)}")
            return jsonify({'error': 'Error updating favorites'}), 500
    except Exception as e:
        current_app.logger.error(f"Error in toggle_favorite: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@main.route('/favorites')
def favorite_events():
    if 'username' not in session:
        flash('Please login to view your favorite events', 'warning')
        return redirect(url_for('main.login'))
        
    if 'user_id' not in session:
        flash('Session error. Please try logging in again.', 'error')
        return redirect(url_for('main.login'))
        
    try:
        # First verify the user exists
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found. Please login again.', 'error')
            return redirect(url_for('main.login'))
            
        # Debug logging
        current_app.logger.info(f"Fetching favorites for user {user.username} (ID: {user.id})")
        
        # Get user's favorite events
        user_events = UserEvent.query.filter_by(user_id=session['user_id']).all()
        events = Event.query.filter(Event.event_id.in_([ue.id for ue in user_events])).all()
        # events = [ue for ue in user_events]
        current_app.logger.info(f"Found {len(user_events)} favorite events in UserEvent table")
        
        events = []
        for ue in user_events:
            try:
                if ue.event:  # Check if the event exists
                    events.append(ue.event)
                    current_app.logger.info(f"Added event to list: {ue.event.name} (ID: {ue.event.event_id})")
                else:
                    current_app.logger.warning(f"Found orphaned UserEvent record (ID: {ue.id})")
                    # Clean up orphaned user_event entries
                    db.session.delete(ue)
            except Exception as event_error:
                current_app.logger.error(f"Error processing event: {str(event_error)}")
                continue
        
        # 100% could clean all of this up and have 1 variable passed that checks all the things but just running into the 11th hour here. 
        favorites = get_favorites(session['user_id'])
        rsvps = get_rsvps(session['user_id'])

        db.session.commit()
        current_app.logger.info(f"Returning {len(events)} events to template")
        return render_template('events/favorites.html', events=events, favorites=favorites, rsvps=rsvps)
        
    except Exception as e:
        current_app.logger.error(f"Error in favorite_events: {str(e)}")
        flash(f'Error getting favorite events. Please try again.', 'error')
        return redirect(url_for('main.index'))


@main.route('/events/<event_id>/rsvp', methods=['POST'])
def toggle_rsvp(event_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401

    try:
        user_id = session['user_id']

        # Get user and event
        user = User.query.get(user_id)
        event = Event.query.filter_by(id=event_id).first()

        if not user or not event:
            return jsonify({'error': 'User or Event not found'}), 404

        # Check or create the UserEvent relationship
        user_event = UserEvent.query.filter_by(user_id=user.id, event_id=event.id).first()

        if user_event:
            # Toggle RSVP
            if user_event.rsvp_status == 'going':
                user_event.rsvp_status = 'interested'
                message = 'Marked as interested'
            else:
                user_event.rsvp_status = 'going'
                message = 'RSVP marked as going'
                if not user_event.is_favorite: # If not already a favorite, mark as going
                    user_event.is_favorite = True
                    db.session.add(user_event) 
                
        else:
            # Create new link with RSVP
            user_event = UserEvent(user_id=user.id, event_id=event.id, is_favorite=True, rsvp_status='going')
            db.session.add(user_event)
            message = 'RSVP marked as going'
        db.session.commit()
        return jsonify({'message': message, 'status': 'success', 'rsvp_status': user_event.rsvp_status=='going',})

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'RSVP Toggle Error: {e}')
        return jsonify({'error': 'An unexpected error occurred'}), 500


@main.route('/rsvp')
def rsvp_events():
    if 'user_id' not in session:
        flash('Please login to view your RSVP events', 'warning')
        return redirect(url_for('main.login'))

    try:
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('main.login'))

        # Get RSVP'd events
        rsvp_links = UserEvent.query.filter_by(user_id=user.id, rsvp_status='going').all()
        events = [link.event for link in rsvp_links if link.event]

        return render_template('events/rsvp.html', events=events)

    except Exception as e:
        current_app.logger.error(f"Error in rsvp_events: {str(e)}")
        flash('Error retrieving RSVP events.', 'danger')
        return redirect(url_for('main.index'))


def get_favorites(user_id):
    # First verify the user exists
    user = User.query.get(user_id)
    if not user:
        flash('User not found. Please login again.', 'error')
        return redirect(url_for('main.login'))
        
    # Debug logging
    current_app.logger.info(f"Fetching favorites for user {user.username} (ID: {user.id})")
    
    # Get user's favorite events
    user_events = UserEvent.query.filter_by(user_id=user_id).all()

    events = []
    for ue in user_events:
        try:
            if ue.event:  # Check if the event exists
                events.append(ue.event)
                current_app.logger.info(f"Added event to list: {ue.event.name} (ID: {ue.event.event_id})")
            else:
                current_app.logger.warning(f"Found orphaned UserEvent record (ID: {ue.id})")
                # Clean up orphaned user_event entries
                db.session.delete(ue)
        except Exception as event_error:
            current_app.logger.error(f"Error processing event: {str(event_error)}")
            continue
    
    return [event.id for event in events if event is not None]

def get_rsvps(user_id):
    
    # First verify the user exists
    user = User.query.get(user_id)
    if not user:
        flash('User not found. Please login again.', 'error')
        return redirect(url_for('main.login'))
    
     # Get RSVP'd events
    rsvp_links = UserEvent.query.filter_by(user_id=user.id, rsvp_status='going').all()
    rsvps = [link.event for link in rsvp_links if link.event]

    return [rsvp.id for rsvp in rsvps if rsvp is not None] 

    











































