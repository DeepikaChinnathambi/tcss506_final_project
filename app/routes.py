#All route definitions
#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Blueprint
from app.users import register_user, validate_login
from app.api import ticketmaster_api
from app.models import Event, UserEvent, User, db
from datetime import datetime

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
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route("/about")
def about():
    return render_template("about.html")

@main.route('/newuser', methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        success, message = register_user(username, password)
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
        username = request.form.get('username')
        password = request.form.get('password')

        success, message = validate_login(username, password)
        if success:
            # Get user_id and store in session
            user = User.query.filter_by(username=username).first()
            session['username'] = username
            session['user_id'] = user.id
            flash(message, 'success')
            return redirect(url_for('main.index'))
        else:
            flash(message, 'danger')
            return redirect(url_for('main.login'))

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

             





















