# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
import os

db = SQLAlchemy()
mail=Mail()
migrate = Migrate()

def create_app():
    app = Flask(__name__)


    # Basic app config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')  # Default to SQLite if not set
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'  # Default to False   
    app.config['TICKETMASTER_API_KEY'] = os.getenv('TICKETMASTER_API_KEY', 'your_ticketmaster_api_key_here')

    
    # Flask-Mail configuration using environment variables
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'hubevent123@gmail.com')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'qxfd irdb knkc kusy')
    app.config['MAIL_DEFAULT_SENDER'] = (
        os.getenv('MAIL_DEFAULT_SENDER_NAME', 'Event Hub'),
        os.getenv('MAIL_DEFAULT_SENDER', 'hubevent123@gmail.com')
    )

    db.init_app(app)

    mail.init_app(app)  #Initialize Mail
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

