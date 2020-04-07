import pytest
from users import app


class TestDevelopmentConfig:
    """ This class is used to test the config variables"""

    @pytest.fixture()
    def create_app(self):
        """ this method is used to create the app"""
        app.config.from_object('users.config.DevelopmentConfig')
        return app

    def test_app_is_develop_valid(self, create_app):
        """ This test method is used to test the  debug value"""
        assert create_app.config['DEBUG'] is True
        assert create_app.config['DEBUG'] is not False

