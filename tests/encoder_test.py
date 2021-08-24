import unittest
import os
import re

from paypalhttp import File
from paypalhttp.encoder import Encoder

from paypalhttp.serializers import Json, FormPart, Text, Multipart, FormEncoded

class GenericRequest:
    pass

def abspath(path):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), path)

class EncoderTest(unittest.TestCase):

    def test_Encoder_serialize_request_throwsWhenHeadersNone(self):
        req = GenericRequest()
        req.body = {
            "key": "value",
            "list": ["one", "two"]
        }

        try:
            Encoder([Json(), Text(), Multipart(), FormEncoded()]).serialize_request(req)
        except Exception as e:
            self.assertIsInstance(e, IOError)
            self.assertEqual("Http request does not have content-type header set", str(e))

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
            Encoder([Json(), Text(), Multipart(), FormEncoded()]).serialize_request(req)
        except Exception as e:
            self.assertIsInstance(e, IOError)
            self.assertTrue("Unable to serialize request with Content-Type application/xml. Supported encodings are " in str(e))

    def test_Encoder_serialize_request_withJsonContentType_stringifysData(self):
        req = GenericRequest()
        req.body = {
            "key": "value",
            "list": ["one", "two"]
        }
        req.headers = {
            "content-type": "application/json; charset=utf8"
        }

        j = Encoder([Json(), Text(), Multipart(), FormEncoded()]).serialize_request(req)

        self.assertTrue('{' in j)
        self.assertTrue('"key": "value"' in j)
        self.assertTrue('"list": ["one", "two"]' in j)

    def test_Encoder_serialize_request_withTextContentType_stringifiesData(self):
        req = GenericRequest()
        req.body = "some text data"
        req.headers = {
            "content-type": "text/plain; charset=utf8"
        }

        b = Encoder([Json(), Text(), Multipart(), FormEncoded()]).serialize_request(req)
        self.assertEqual(req.body, b)

    def test_Encoder_serialize_request_withMultipartContentType_stringifysData(self):
        request = GenericRequest()
        request.path = "/"
        request.verb = "POST"
        request.headers = {"content-type": "multipart/form-data; charset=utf8"}
        f = File(abspath('tests/resources/fileupload_test_binary.jpg'))
        data = f.read()

        request.body = {"some_key": "some_value", "some_nested[key]": "some_nested_value", "file": f}

        serialized = Encoder([Json(), Text(), Multipart(), FormEncoded()]).serialize_request(request)
        self.assertTrue("multipart/form-data; boundary=" in request.headers["content-type"])

        self.assertTrue("Content-Disposition: form-data; name=\"some_key\"" in serialized)
        self.assertTrue("some_value" in serialized)
        self.assertTrue("Content-Disposition: form-data; name=\"some_nested[key]\"" in serialized)
        self.assertTrue("some_nested_value" in serialized)
        self.assertTrue("Content-Disposition: form-data; name=\"file\"; filename=\"fileupload_test_binary.jpg\"" in serialized)
        self.assertTrue("Content-Type: image/jpeg" in serialized)
        self.assertTrue(str(data) in serialized)

        f.close()

    def test_Encoder_serialize_request_withMultipartContentType_encodesFormPart(self):
        request = GenericRequest()
        request.path = "/"
        request.verb = "POST"
        request.headers = {"content-type": "multipart/form-data; charset=utf8"}
        f = File(abspath('tests/resources/fileupload_test_binary.jpg'))
        data = f.read()

        request.body = {
            "file": f,
            "input": FormPart({"key": "val"}, {"Content-Type": "application/json"})
        }

        serialized = Encoder([Json(), Text(), Multipart(), FormEncoded()]).serialize_request(request)
        self.assertTrue("multipart/form-data; boundary=" in request.headers["content-type"])

        self.assertTrue("Content-Disposition: form-data; name=\"input\"; filename=\"input.json\"" in serialized)
        self.assertTrue("{\"key\": \"val\"}" in serialized)
        self.assertTrue("Content-Disposition: form-data; name=\"file\"; filename=\"fileupload_test_binary.jpg\"" in serialized)
        self.assertTrue("Content-Type: image/jpeg" in serialized)
        self.assertTrue(str(data) in serialized)
        self.assertIsNotNone(re.search('.*input.json.*fileupload_test_binary.jpg.*', serialized, re.MULTILINE | re.DOTALL))

        f.close()

    def test_Encode_serialize_request_withFormEncodedContentType_stringifysData(self):
        request = GenericRequest()
        request.path = "/"
        request.verb = "POST"
        request.headers = {"content-type": "application/x-www-form-urlencoded; charset=utf8"}
        request.body = {
            'key': 'value',
            'key_two': 'value with spaces'
        }

        serialized = Encoder([Json(), Text(), Multipart(), FormEncoded()]).serialize_request(request)
        self.assertIsNotNone(re.match('(key=value&key_two=value%20with%20spaces|key_two=value%20with%20spaces&key=value)', serialized))

    def test_Encoder_deserialize_response_throwsWhenHeadersNone(self):
        j = '{"key": "value", "list": ["one", "two"]}'

        headers = None

        try:
            b = Encoder([Json(), Text(), Multipart(), FormEncoded()]).deserialize_response(j, headers)
        except IOError as e:
            self.assertIsInstance(e, IOError)
            self.assertEqual("Http response does not have content-type header set", str(e))

    def test_Encoder_deserialize_response_throwsWhenContentTypeNotSupported(self):
        j = '{"key": "value", "list": ["one", "two"]}'

        headers = {"content-type": "application/xml"}

        try:
            b = Encoder([Json(), Text(), Multipart(), FormEncoded()]).deserialize_response(j, headers)
        except IOError as e:
            self.assertIsInstance(e, IOError)
            self.assertTrue("Unable to deserialize response with content-type application/xml. Supported decodings are " in str(e))

    def test_Encoder_deserialize_response_text(self):
        j = 'some plain text'
        headers = {"content-type": "text/plain"}

        b = Encoder([Json(), Text(), Multipart(), FormEncoded()]).deserialize_response(j, headers)

        self.assertEqual(j, b)

    def test_Encoder_deserialize_response_text_case_insensitive(self):
        j = 'some plain text'
        headers = {"content-type": "TEXT/plain"}

        b = Encoder([Json(), Text(), Multipart(), FormEncoded()]).deserialize_response(j, headers)

        self.assertEqual(j, b)

    def test_Encoder_deserialize_response_Json(self):
        j = '{"key": "value", "list": ["one", "two"]}'

        headers = {"content-type": "application/json"}

        b = Encoder([Json(), Text(), Multipart(), FormEncoded()]).deserialize_response(j, headers)

        self.assertEqual("value", b["key"])
        self.assertEqual(["one", "two"], b["list"])

    def test_Encoder_deserialize_response_Json_case_insensitive(self):
        j = '{"key": "value", "list": ["one", "two"]}'

        headers = {"content-type": "application/JSON"}

        b = Encoder([Json(), Text(), Multipart(), FormEncoded()]).deserialize_response(j, headers)

        self.assertEqual("value", b["key"])
        self.assertEqual(["one", "two"], b["list"])

    def test_Encoder_deserialize_response_multipart(self):
        j = 'some plain text'
        headers = {"content-type": "multipart/form-data"}

        try:
            b = Encoder([Json(), Text(), Multipart(), FormEncoded()]).deserialize_response(j, headers)
            self.fail('deserialize should have thrown with content-type multipart')
        except IOError as e:
            self.assertTrue('Multipart does not support deserialization', str(e))

    def test_Encoder_deserialize_response_formEncoded(self):
        data = 'key=value&key_two=value%20with%20spaces'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            b = Encoder([Json(), Text(), Multipart(), FormEncoded()]).deserialize_response(data, headers)
            self.fail('deserialize should have thrown with content-type formencoded')
        except IOError as e:
            self.assertTrue('FormEncoded does not support deserialization', str(e))

