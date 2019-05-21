"""
Author: Tyler Puleo
License: GPL
Version: 0.0.1
Maintainer: Tyler Puleo
Status: Production
Summary: This is the management script that runs the spark app.
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
import os

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
