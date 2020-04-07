from flask import jsonify
import jwt
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from users import app, mail


def generate_token(email):
    """ This method is used generate the token"""
    serializer = URLSafeTimedSerializer(secret_key=app.config['SECRET_KEY'])  # used user secrete key
    token = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])  # user security password salt
    return token


def confirm_token(token, expiration=180):
    """ This method is used to confirm the token within expiration time """
    serializer = URLSafeTimedSerializer(secret_key=app.config['SECRET_KEY'])  # using secrete key
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],  # using password security salt
            max_age=expiration,  # assign max time
        )
    except:
        return None  # if invalid return None
    return email  # if valid return email


def create_jwt_token(id):
    """ This method is used to create jwt token"""
    try:
        payload = {'id': id, 'exp': datetime.utcnow() + timedelta(seconds=10000)}
        encoded_token = jwt.encode(payload, app.config['SECRET_KEY'], 'HS256').decode('utf-8')
    except:
        return None  # if invalid data return None
    return encoded_token  # return encoded token


def decode_jwt_token(token):
    """ This method is used to decode the jwt token"""
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return None  # if invalid data return None
    return decoded_token  # return decode token


def json_response(message):
    """ This method is used to return the json response"""
    data = {'message': message}
    return jsonify(data)


def send_email(to, subject, template):
    """ This method is used to create the send the email"""
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

