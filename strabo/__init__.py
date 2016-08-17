'''
GOAL:

Creates properly configured Flask "app" object and flask_sqlalchemy.SQLAlchemy "db"
object at the package level, so they can be fetched with:

from strabo import app, db

From any file in the package.

Also creates an empty configuration dictionary, straboconfig, which is filled in
with configuration information when the package is used, in files like runserver.py.
It is not filled here because it cranshes when documentation is being built.

Then it loads the views package so that flask knows where to send browser requests.
'''

import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

config.config_app(app)

db = SQLAlchemy(app)

straboconfig = config.get_config_info()

import strabo.views
