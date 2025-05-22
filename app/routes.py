#All route definitions
#!/usr/bin/env python3
from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from .models import User, db
from .users import register_user, validate_login

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
        password = request.form.get('password')

        success, message = register_user(username, password)
        if success:
            flash(message, 'success')
            return redirect(url_for('main.login'))  # Assume you have a login route
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
            session['username'] = username
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

             





















