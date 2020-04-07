import os
from dotenv import load_dotenv
load_dotenv()
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from users import app, db

app.config.from_object(os.getenv('USER_APP_SETTINGS'))

migrate = Migrate(app, db)
server = Manager(app)

# migrations
server.add_command('db', MigrateCommand)


@server.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@server.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    server.run()
