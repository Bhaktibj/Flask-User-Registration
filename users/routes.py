# import name
from flask import request
from flask import render_template
from flask_login import logout_user
from users.common.utils import json_response
from flask import Blueprint
from users.services.user_service import UserService

user_app = Blueprint('user', __name__)  # created blue-print
user = UserService()  # created user object


@user_app.route('/')
def home():
    """ This method is used to render the home page"""
    try:
        return render_template('home.html')
    except:
        return json_response("something went wrong please check")


@user_app.route('/register', methods=('GET', 'POST'))
def register():
    """This method is used to register for the user """
    try:
        if request.method == 'POST':  # if request is post
            user.for_registration(request_data=request.form)  # validate data
        return render_template("user/register.html")  # render the register page
    except:
        return render_template("home.html")  # except render the home page


@user_app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    """ This method is used to confirm the registration through email"""
    try:
        user.for_confirm_email(token=token)  # pass token to confirmation service and return response
    except:
        return render_template('home.html')  # render home page
    return render_template('user/register.html')  # render register


@user_app.route('/login', methods=('GET', 'POST'))
def login():
    """ this method is used to login the user"""
    try:
        if request.method == 'POST': # if request method is post
            user.for_login(request_data=request.form)  # pass the request form data to user login service
        return render_template('user/login.html')  # render login page
    except:
        return render_template('home.html')  # except render the home page


@user_app.route('/logout')
def logout():
    """ This method is used to logout user"""
    try:
        logout_user()  # using built in function logout user
    except:
        return render_template('user/login.html')
    return render_template('home.html')


@user_app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    """ This method is used to forgot password"""
    try:
        if request.method == 'POST': # if request method == 'POST'
            user.for_forgot_password(request_data=request.form) # pass form data to service
        return render_template('user/forgot.html')
    except:
        return render_template('home.html')


@user_app.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    """ This method is used to reset password token """
    try:
        if request.method == 'POST':  # check request method is post
            user.for_reset_password(token=token) # pass the token service
        return render_template('user/reset_password.html')
    except:
        return render_template('home.html')


@user_app.route('/change_pass', methods=['GET', 'POST'])
def change_password():
    """ This method is used to change the password """
    try:
        if request.method == 'POST':  # if request method is POST
            user.for_change_password(request_data=request.form)  # send data to post service
        return render_template('user/change_password.html')
    except:
        return render_template('home.html')


