import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
base_url = os.getenv('USER_APP_BASE_URL')


class TestUserApi:
    def test_registration_valid_data(self):
        """ This method is used to test the user registration"""
        url = base_url + '/register'
        data = {'title': 'miss', 'username': 'nikita', 'email': 'nikit.pawar05@gmail.com',
                'phone_number': '9008678790',
                'password': 'nikita@123', 'confirm_password': 'nikita@123', 'country': 'India'}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(response.text)
        assert response.status_code == 200

    def test_registration_invalid_data(self):
        """ This method is used to test the user registration to give invalid data"""
        url = base_url + '/login'
        data = {'title': 'miss', 'username': 'nikita',
                'phone_number': '9008678790',
                'password': 'nikita@123', 'confirm_password': 'nikita@123', 'country': 'India'}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(response.text)
        assert response.status_code == 200

    def test_login_valid_data(self):
        """ This method is used to test the user to give valid data"""
        url = base_url + '/login'
        data = {'username': 'nikita',
                'password': 'nikita@123'}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(response.text)
        assert response.status_code == 200

    def test_forgot_valid_data(self):
        """ This method is used to test the forgot password"""
        url = base_url + '/forgot'
        data = {'email':'nikita.pawar005@gmail.com'}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(response.text)
        assert response.status_code == 200


