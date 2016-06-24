from flask import Flask
from strabo import config_canyon
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

config_canyon.config_app(app)

db = SQLAlchemy(app)

import strabo.views
