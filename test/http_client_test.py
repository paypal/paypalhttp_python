import unittest
from unit_test_utils import *
from braintreehttp import HttpClient, Injector
import requests
import json

class JsonHttpClient(HttpClient):

    def parse_response_body(self, response):
        return json.loads(response.text)


class HttpClientTest(unittest.TestCase):
    @responses.activate
    def test_HttpClient_execute_addsHeaders(self):
        client = HttpClient()
        request = requests.Request("GET", "http://localhost/")
        stub_request_with_empty_reponse(request)

        client.execute(request)
        self.assertEqual(request.headers["User-Agent"], client.get_user_agent())

    @responses.activate
    def test_HttpClient_addInjector_usesInjector(self):
        client = HttpClient()

        class TestInjector(Injector):
            def __call__(self, request):
                request.headers["Foo"] = "Bar"

        client.add_injector(TestInjector())

        request = requests.Request("GET", "http://localhost/")
        stub_request_with_empty_reponse(request)

        client.execute(request)

        self.assertEqual(request.headers["Foo"], "Bar")

    @responses.activate
    def test_HttpClient_execute_usesAllParamsInRequest_plaintextdata(self):
        client = HttpClient()
        request = requests.Request("POST", "http://examplehost/", headers={"Test": "Header"}, data="Some data")
        stub_request_with_empty_reponse(request)

        client.execute(request)

        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0].request
        self.assertEqual(call.method, "POST")
        self.assertEqual(call.url, "http://examplehost/")
        self.assertEqual(call.headers["Test"], "Header")
        self.assertEqual(call.body, "Some data")

    @responses.activate
    def test_HttpClient_execute_usesAllParamsInRequest_json(self):
        client = HttpClient()
        request = requests.Request("POST", "http://examplehost/", headers={"Test": "Header"}, json={"some": "data"})
        stub_request_with_empty_reponse(request)

        client.execute(request)

        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0].request
        self.assertEqual(call.method, "POST")
        self.assertEqual(call.url, "http://examplehost/")
        self.assertEqual(call.headers["Test"], "Header")
        self.assertEqual(call.body, "{\"some\": \"data\"}")

    @responses.activate
    def test_HttpClient_onError_throwsCorrectExceptionForStatusCode(self):
        client = HttpClient()

        request = requests.Request("POST", "http://examplehost/error")
        stub_request_with_response(request, "", 400)

        try:
            client.execute(request)
        except BaseException as e:
            self.assertEqual("APIException", e.__class__.__name__)

    @responses.activate
    def test_HttpClient_onSuccess_returnsResponse_with_empty_body(self):
        client = JsonHttpClient()

        request = requests.Request("GET", "http://localhost/")
        stub_request_with_response(request, "", 204)

        try:
            response = client.execute(request)
            self.assertIsNone(response.result)
        except BaseException as exception:
            self.fail(exception.message)

    @responses.activate
    def test_HttpClient_onSuccess_returnsResponse_with_invalid_json_body(self):

        class DeserializingHttpClient(HttpClient):
            def parse_response_body(self, response):
                return "Some data"

        client = DeserializingHttpClient()

        request = requests.Request("GET", "http://localhost/")
        stub_request_with_response(request, "not some data", 201)

        try:
            response = client.execute(request)
            self.assertEqual(response.result, "Some data")
        except BaseException as exception:
            self.fail(exception.message)

    @responses.activate
    def test_HttpClient_onSuccess_escapesDashesWhenUnmarshaling(self):
        client = JsonHttpClient()

        request = requests.Request("GET", "http://localhost/")
        stub_request_with_response(request, "{\"valid-key\": \"valid-data\"}", 201)

        try:
            response = client.execute(request)
            self.assertEqual(response.result.valid_key, "valid-data")
        except BaseException as exception:
            self.fail(exception.message)


if __name__ == '__main__':
    unittest.main()
