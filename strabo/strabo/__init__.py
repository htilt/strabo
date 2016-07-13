from flask import Flask
from strabo import config_canyon
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

import strabo.views
