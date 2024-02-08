import pytest

from backend.api.app import app


@pytest.fixture()
def app_test():
    print('INIT APP')
    yield app


@pytest.fixture()
def client(app_test):
    return app_test.test_client()
