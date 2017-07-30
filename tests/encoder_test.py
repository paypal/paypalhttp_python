import unittest
from braintreehttp.encoder import Encoder

class GenericRequest:
    pass

class EncoderTest(unittest.TestCase):

    def test_Encoder_serialize_request(self):
        req = GenericRequest()
        req.body = {
            "key": "value",
            "list": ["one", "two"]
        }
        req.headers = {
            "Content-Type": "application/json"
        }

        j = Encoder().serialize_request(req)

        self.assertTrue('{' in j)
        self.assertTrue('"key": "value"' in j)
        self.assertTrue('"list": ["one", "two"]' in j)

    def test_Encoder_serialize_request_throwsWhenHeadersNone(self):
        req = GenericRequest()
        req.body = {
            "key": "value",
            "list": ["one", "two"]
        }

        try:
            Encoder().serialize_request(req)
        except Exception as e:
            self.assertIsInstance(e, IOError)
            self.assertEqual("Http request does not have Content-Type header set", str(e))

    def test_Encoder_serialize_request_throwsWhenContentTypeNotJson(self):
        req = GenericRequest()
        req.body = {
            "key": "value",
            "list": ["one", "two"]
        }
        req.headers = {
            "Content-Type": "application/xml"
        }

        try:
            Encoder().serialize_request(req)
        except Exception as e:
            self.assertIsInstance(e, IOError)
            self.assertEqual("Unable to serialize request with Content-Type application/xml. Supported encodings are [application/json]", str(e))

    def test_Encoder_deserialize_response(self):
        j = '{"key": "value", "list": ["one", "two"]}'

        headers = {"Content-Type": "application/json"}

        b = Encoder().deserialize_response(j, headers)

        self.assertEqual("value", b["key"])
        self.assertEqual(["one", "two"], b["list"])

    def test_Encoder_deserialize_response_throwsWhenHeadersNone(self):
        j = '{"key": "value", "list": ["one", "two"]}'

        headers = None

        try:
            b = Encoder().deserialize_response(j, headers)
        except IOError as e:
            self.assertIsInstance(e, IOError)
            self.assertEqual("Http response does not have Content-Type header set", str(e))

    def test_Encoder_deserialize_response_throwsWhenContentTypeNotJson(self):
        j = '{"key": "value", "list": ["one", "two"]}'

        headers = {"Content-Type": "application/xml"}

        try:
            b = Encoder().deserialize_response(j, headers)
        except IOError as e:
            self.assertIsInstance(e, IOError)
            self.assertEqual("Unable to deserialize response with Content-Type application/xml. Supported decodings are [application/json]", str(e))

