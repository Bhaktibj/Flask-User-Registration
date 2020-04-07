import datetime
from flask import request, url_for, flash, render_template
from flask_login import login_user, current_user
from users.common.utils import json_response, generate_token, confirm_token, create_jwt_token, send_email
from users import db, bcrypt
from users.models.models import User


class UserService:
    """ This service class is used to create the user-registration, login, forgot password etc"""

    def for_registration(self, request_data):
        """ This method is used to user registration"""
        try:
            title = request_data.get('title')  # get form input title
            username = request_data.get('username')  # get form input username
            email = request_data.get('email')  # get form input email
            phone_number = request_data.get('phone_number')
            country = request_data.get('country')
            password = request_data.get('password')
            confirm_password = request_data.get('confirm_password')
            # check all fields are not None or not
            if title and username and email and phone_number and country and password and confirm_password is not None:
                if password == confirm_password:  # check password and confirm_password is equal or not
                    user = User.query.filter_by(email=email).first()  # if password equal check user is exist in db or not
                    if not user:  # if not user
                        user = User(title=title, username=username, email=email, password=password,
                                    phone_number=phone_number,
                                    country=country, confirmed=False)
                        db.session.add(user)  # add the user
                        db.session.commit()  # commit
                        token = generate_token(email=user.email)  # generate token using user.email
                        confirm_url = url_for('user.confirm_email', token=token, _external=True)  # create confirm url
                        html = render_template('user/activate.html', confirm_url=confirm_url)
                        subject = "Please confirm your registration email"
                        send_email(user.email, subject, html)  # send mail to the user
                        flash('A confirmation email has been sent via email.', 'success')  # if mail sent
                    else:  # if user already exists
                        flash("Username and Email is already exist, please try another email and username", 'danger')
                else:  # if password is mismatch
                    flash("password is mismatch please enter correct password", 'danger')
            else:   # if fields are None
                flash('All fields are required', 'danger')
        except:  # if something went wrong
            flash("something went wrong, please try later", 'danger')

    def for_confirm_email(self, token):
        """ This service method is used to confirm the user registration"""
        try:  # enter the try block
            email = confirm_token(token)  # confirm the token
            if email is not None:   # check email is not None or not
                user = User.query.filter_by(email=email).first_or_404()  # if email check email is exists in db or not
                if user and not user.confirmed:  # check if user and user.confirmed == False
                    user.confirmed = True  # user.confirmed == True
                    user.confirmed_on = datetime.datetime.now()  # update confirmed time
                    db.session.add(user)  # add user
                    db.session.commit()  # commit
                    flash('You have confirmed your account', 'success')  # if confirm user
                else:  # if user already confirm user
                    flash('already confirmed your account', 'success')
            else:  # confirm url is expired
                flash('The confirmation link is invalid or has expired.', 'danger')
        except:  # something went wrong
            flash('something went wrong', 'danger')

    def for_login(self, request_data):
        """ This method is used to login user"""
        try:
            username = request_data.get('username')  # take form input username
            password = request_data.get('password')  # take from input password
            if username and password is not None:  # if username and password is not None
                user = User.query.filter_by(username=username).first_or_404()  # filter username is exists in db or not
                if user and user.check_password(password):  # if user and user.password
                    login_user(user)  # login user
                    token = create_jwt_token(id=user.id)  # create jwt token
                    flash("login successfully " + token, 'success')  # if login user
                else:
                    flash('Invalid username or password.', 'danger')  # if invalid username & password
            else:
                flash('Username and password is required', 'danger')  # if username & password is None
        except:
            flash("something went wrong", 'danger')  # if anything wrong

    def for_forgot_password(self, request_data):
        """ This method is used to forgot password"""
        try:
            email = request_data.get('email')  # take form input email
            user = User.query.filter_by(email=email).first_or_404()  # check email is exists or  not
            if user:   # if user
                token = generate_token(user.email)  # generate token using email
                user.password_reset_token = token  # assign password_reset_token == token
                db.session.commit()  # commit user
                reset_url = url_for('user.reset', token=token, _external=True)  # create reset password url
                html = render_template('user/reset.html',
                                       username=user.email,
                                       reset_url=reset_url)
                subject = "Reset your password"
                send_email(user.email, subject, html)  # send mail to the user
                flash('A password reset email has been sent via email.', 'success')  # if sent mail
            else:
                flash('Does not exist user, please enter valid email id', 'danger')  # else does not exist user
        except:
            flash("something went wrong", 'danger')  # something went wrong

    def for_reset_password(self, token):
        """This method is used to reset password """
        try:
            email = confirm_token(token)  # confirm token and return email
            if email is not None:  # if email is not None
                user = User.query.filter_by(email=email).first_or_404()  # check email is exist or not
                if user is not None:  # if user is not None
                    password = request.form.get('password')  # request form input from user
                    confirm_password = request.form.get('confirm_password')  # request form input confirm password
                    if password == confirm_password:  # check password and confirm password is equal or not
                        user.password = password  # if equal assigned password = password
                        user.password_reset_token = None  # password reset token is none
                        db.session.add(user)  # add user
                        db.session.commit()  # commit
                        flash('password reset successfully', 'success')  # if reset password
                    else:
                        flash('password is mismatch', 'danger')  # if password and confirm password is mismatch
                else:
                    flash('does not exist user', 'danger')  # if not user
            else:
                flash('The reset password link is invalid or has expired.', 'danger')  # if link is expired
        except:
            flash('something went wrong', 'danger')  # if anything wrong

    def for_change_password(self, request_data):
        """ This method is used to change password """
        try:
            if current_user.is_authenticated:  # check current user is authenticated or not
                password = request_data.get('password')  # request form input password
                confirm_password = request_data.get('confirm_password')  # request form input confirm password
                if password and confirm_password is not None:  # check password and confirm password is not None or not
                    if password == confirm_password:  # if password and confirm password is equal or not
                        current_user.password = password  # assigned password to new password
                        db.session.add(current_user)  # add user
                        db.session.commit()  # commit
                        flash('password changed successfully', 'success')  # if commit
                    else:
                        flash('password is mismatch', 'danger')  # if password and confirm password is mismatch
                else:
                    flash('field value is required', 'danger')  # if field value is none
            else:
                flash('you need to login first', 'danger')  # if user is not authenticated
        except:
            flash('something went wrong', 'danger')  # if something went wrong

