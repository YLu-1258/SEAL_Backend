from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

"""
These object can be used throughout project.
1.) Objects from this file can be included in many blueprints
2.) Isolating these object definitions avoids duplication and circular dependencies
"""
login_manager = LoginManager()

# Setup of key Flask object (app)
app = Flask(__name__)
# Setup SQLAlchemy object and properties for the database (db)
dbURI = 'sqlite:////volumes/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy(app)
login_manager.init_app(app)
Migrate(app, db)

reviews_app = Flask(__name__)
# Setup SQLAlchemy object and properties for the database (db)
dbURI = 'sqlite:////volumes/reviews.db'
reviews_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
reviews_app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
reviews_app.config['SECRET_KEY'] = 'SECRET_KEY'
reviews_db = SQLAlchemy(reviews_app)
Migrate(reviews_app, reviews_db)

# # Images storage
# app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # maximum size of uploaded content
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']  # supported file types
# app.config['UPLOAD_FOLDER'] = 'volumes/uploads/'  # location of user uploaded content
