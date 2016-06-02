from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from strabo import config_canyon


app = Flask(__name__)

config_canyon.config_app(app)

db = SQLAlchemy(app)


import strabo.views
