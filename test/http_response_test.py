import unittest
from braintreehttp import *


class HttpResponseTest(unittest.TestCase):
    def test_HttpResponse_constructor_setsParamsCorrectly(self):
        resp = HttpResponse("data", 200, {"header": "value"})
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.headers)
        self.assertEqual(resp.headers["header"], "value")
        self.assertEqual(resp.result, "data")

    def test_HttpResponse_constrctor_withStringData_lenZero_ResultIsNone(self):
        resp = HttpResponse("", {})
        self.assertIsNone(resp.result)

    def test_HttpResponse_constructor_withDictData_ResultIsObject(self):
        object = {
            "int": 100,
            "str": "value",
            "nested": {
                "key-one": "value-one",
                "key-two": 123.456
            }
        }

        resp = HttpResponse(object, 200)
        self.assertEqual(resp.result.int, 100)
        self.assertEqual(resp.result.str, "value")
        self.assertEqual(resp.result.nested.key_one, "value-one")
        self.assertEqual(resp.result.nested.key_two, 123.456)

    def test_HttpResponse_constrctor_withDictData_lenZero_ResultIsNone(self):
        resp = HttpResponse({}, 200)
        self.assertIsNone(resp.result)


if __name__ == '__main__':
    unittest.main()
