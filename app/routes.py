#All route definitions
#!/usr/bin/env python3
from flask import Flask, render_template,request,redirect,url_for,session,flash
from users import register_user,validate_login

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         if request.form['username'] == USER['username'] and request.form['password'] == USER['password']:
#             session['username'] = request.form['username']
#             return redirect(url_for('home'))
#         return "Invalid credentials. <a href='/login'>Try again</a>"
#     return '''
#         <form method="post">
#             Username: <input type="text" name="username"><br>
#             Password: <input type="password" name="password"><br>
#             <input type="submit" value="Login">
#         </form>
#     '''

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        success, message = register_user(username, password)
        if success:
            print(f"[INFO] SUCCESS register user: {username}")
            flash(message, 'success')
            return redirect(url_for('login'))  # Assume you have a login route
        else:
            flash(message, 'danger')
            return render_template('register.html')

@app.route('/loginvalidate', methods=['GET', 'POST'])
def loginvalidate():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        success, message = validate_login(username, password)
        if success:
            session['username'] = username
            flash(message, 'success')
            return redirect(url_for('index'))
        else:
            flash(message, 'danger')
            return redirect(url_for('login'))
   

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    else:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('login'))

             

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)






















if __name__ == '__main__':
    app.run(debug=True)

