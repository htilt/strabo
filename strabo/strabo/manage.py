import os

from strabo import app
from strabo import db

from strabo import config_canyon
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

migrate = Migrate(app,db) #migrate instance
manager = Manager(app)

manager.add_command('db',MigrateCommand) #run migrations from the command line

if __name__ == '__main__':
	manager.run()