from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from sqlalchemy import create_engine
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)


from app import views, models
