from app import db, app
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

# Database migration code // Flask-Migrate
# http://flask-migrate.readthedocs.org/en/latest/
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()