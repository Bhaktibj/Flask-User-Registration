import pymysql
import datetime
pymysql.install_as_MySQLdb()
from users import db, bcrypt


class User(db.Model):
    """ Class User model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    country = db.Column(db.String(30))
    password = db.Column(db.String(100), nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    password_reset_token = db.Column(db.String(100), nullable=True, default=None)

    def __init__(self,username, email,  password=None, **kwargs):
        """ Create instance"""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.password = self.set_password(password=password)
        else:
            self.password = None
        self.registered_on = datetime.datetime.now()

    def set_password(self, password):
        """ the hashed password"""
        return bcrypt.generate_password_hash(password)

    def check_password(self, hashed_password):
        """ check password"""
        return bcrypt.check_password_hash(self.password, hashed_password)

    def is_authenticated(self):
        """ User is authenticated"""
        return True

    def is_active(self):
        """ is active"""
        return True

    def get_id(self):
        """ get id"""
        return self.id

    def __repr__(self):
        """ get email"""
        return self.email