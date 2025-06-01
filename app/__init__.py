# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail 

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Basic app config
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'hubevent123@gmail.com'
    app.config['MAIL_PASSWORD'] = 'qxfd irdb knkc kusy'
    app.config['MAIL_DEFAULT_SENDER'] = ('Event Hub', 'hubevent123@gmail.com')

    db.init_app(app)
    mail.init_app(app)  #Initialize Mail

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

