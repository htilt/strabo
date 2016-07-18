'''
GOAL:

Creates properly configured Flask "app" object and flask_sqlalchemy.SQLAlchemy "db" object at the package level, so they can be fetched with

from strabo import app, db

From any file in the package.

Then it loads the views package so that flask knows where to send browser requests.
'''

import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

config.config_app(app)

db = SQLAlchemy(app)

straboconfig = dict()#is populated in runserver.py

import strabo.views