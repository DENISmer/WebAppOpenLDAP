from flask_restful import Resource
import functools


class ItemAPI(Resource):
    init_every_request = False

    def get(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass


class GroupAPI(Resource):
    init_every_request = False

    def get(self, username_uid, *args, **kwargs):
        pass

    def post(self, username_uid, *args, **kwargs):
        pass


def decorator_test(func):

    @functools.wraps(func)
    def wraps(*args, **kwargs):

        print('wrap start')
        res = func(*args, **kwargs)
        print('wrap end')

        return res

    return wraps


class TestA:
    @decorator_test
    def create(self):
        print('func create.')


class TestInherited(TestA):

    def create(self):
        print('func create inh.')


test_inherited = TestInherited()
test_inherited.create()
