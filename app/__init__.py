from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from sqlalchemy import create_engine
import os
#template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__)
app.config.from_object('config')
app.config['DEBUG'] = True
db = SQLAlchemy(app)
login_manager = LoginManager(app)


from app import views, models
