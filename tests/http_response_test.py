import unittest
from braintreehttp import HttpResponse


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

    def test_HttpResponse_constructor_withDictData_listOfStrings(self):
        object = {
            "int": 100,
            "str": "value",
            "list": ["values"],
        }

        resp = HttpResponse(object, 200)
        self.assertEqual(resp.result.int, 100)
        self.assertEqual(resp.result.str, "value")
        self.assertEqual(resp.result.list[0], "values")

    def test_HttpResponse_constructor_withDictData_listOfObjects(self):
        object = {
            "int": 100,
            "str": "value",
            "list": [{
                "key": "value",
                "key_two": "value_two"
            }],
        }

        resp = HttpResponse(object, 200)
        self.assertEqual(resp.result.int, 100)
        self.assertEqual(resp.result.str, "value")
        self.assertEqual(resp.result.list[0].key, "value")
        self.assertEqual(resp.result.list[0].key_two, "value_two")

    def test_HttpResponse_constructor_withDictData_listOfLists(self):
        object = {
            "int": 100,
            "str": "value",
            "list": [
                [
                    {
                        "key": "value",
                        "key_two": ["value_two"]
                    }
                ],
                [
                    {
                        "key_three": "value_three",
                        "key_four": "value_four"
                    }
                ]
            ],
        }

        resp = HttpResponse(object, 200)
        self.assertEqual(resp.result.int, 100)
        self.assertEqual(resp.result.str, "value")
        self.assertEqual(resp.result.list[0][0].key, "value")
        self.assertEqual(resp.result.list[0][0].key_two[0], "value_two")
        self.assertEqual(resp.result.list[1][0].key_three, "value_three")
        self.assertEqual(resp.result.list[1][0].key_four, "value_four")

    def test_HttpResponse_constrctor_withDictData_lenZero_ResultIsNone(self):
        resp = HttpResponse({}, 200)
        self.assertIsNone(resp.result)


if __name__ == '__main__':
    unittest.main()
