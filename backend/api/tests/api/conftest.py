import pytest

from backend.api.app import app
from backend.api.config import ldap


@pytest.fixture()
def app_test():
    # print('INIT APP')
    app.config.update(
        HOSTS=['0.0.0.0'],
        LDAP_PORT=8389,
        SQLALCHEMY_DATABASE_URI=f'sqlite:///test_db.db'
    )
    ldap.config['LDAP_PORT'] = 8389
    ldap.config['LDAP_HOSTS'] = ['0.0.0.0']

    yield app


@pytest.fixture()
def client(app_test):
    return app_test.test_client()
