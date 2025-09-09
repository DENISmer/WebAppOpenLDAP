import unittest

from api.common.getting_free_id import FreeIdGetter


class TestFreeIdNumberGetter(unittest.TestCase):
    def test_empty_number_list(self):
        free_id = FreeIdGetter(None)
        result = free_id.get_free_spaces([])
        self.assertEqual(result, 10000)
        free_id.remove_all()

    def test_number_list_values_least_10000(self):
        free_id = FreeIdGetter(None)
        result = free_id.get_free_spaces([9999, 110, 124, 1000, 9999])

        self.assertEqual(result, 10000)

        free_id.remove_all()

    def test_get_free_id_in_list(self):
        free_id = FreeIdGetter(None)

        free_id.remove_all()

        input_list = [10001, 10002, 10006]

        result = free_id.get_free_spaces(input_list)
        self.assertEqual(result, 10003)

        result = free_id.get_free_spaces(input_list)
        self.assertEqual(result, 10004)

        result = free_id.get_free_spaces(input_list)
        self.assertEqual(result, 10005)

        free_id.remove_all()

    def test_get_free_id_out_list(self):
        free_id = FreeIdGetter(None)

        free_id.remove_all()

        input_list = [10001, 10002, 10003, 10004, 10005, 10006]

        result = free_id.get_free_spaces(input_list)
        self.assertEqual(result, 10007)

        result = free_id.get_free_spaces(input_list)
        self.assertEqual(result, 10008)

        result = free_id.get_free_spaces(input_list)
        self.assertEqual(result, 10009)

        free_id.remove_all()
