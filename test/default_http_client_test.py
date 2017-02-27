import unittest
from unit_test_utils import *
from braintreehttp import DefaultHttpClient, Injector
import requests


class DefaultHttpClientTest(unittest.TestCase):
    @responses.activate
    def test_DefaultHttpClient_execute_addsDefaultHeaders(self):
        client = DefaultHttpClient()
        request = requests.Request("GET", "http://localhost/")
        stub_request_with_empty_reponse(request)

        client.execute(request)
        self.assertEqual(request.headers["User-Agent"], client.get_user_agent())

    @responses.activate
    def test_DefaultHttpClient_addInjector_usesInjector(self):
        client = DefaultHttpClient()

        class TestInjector(Injector):
            def __call__(self, request):
                request.headers["Foo"] = "Bar"

        client.add_injector(TestInjector())

        request = requests.Request("GET", "http://localhost/")
        stub_request_with_empty_reponse(request)

        client.execute(request)

        self.assertEqual(request.headers["Foo"], "Bar")

    @responses.activate
    def test_DefaultHttpClient_execute_usesAllParamsInRequest_plaintextdata(self):
        client = DefaultHttpClient()
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
    def test_DefaultHttpClient_execute_usesAllParamsInRequest_json(self):
        client = DefaultHttpClient()
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
    def test_DefaultHttpClient_onError_throwsCorrectExceptionForStatusCode(self):
        test_table = {
            401: "AuthenticationError",
            403: "AuthorizationError",
            400: "BadRequestError",
            404: "ResourceNotFoundError",
            422: "UnprocessableEntityError",
            426: "UpgradeRequiredError",
            429: "RateLimitError",
            500: "InternalServerError",
            503: "DownForMaintenanceError"
        }

        client = DefaultHttpClient()

        for status_code, error_class in test_table.iteritems():
            request = requests.Request("POST", "http://examplehost/" + error_class)
            stub_request_with_response(request, "", status_code)

            try:
                client.execute(request)
            except BaseException as e:
                self.assertEqual(error_class, e.__class__.__name__)

    @responses.activate
    def test_DefaultHttpClient_onSuccess_returnsResponse_with_empty_body(self):
        client = DefaultHttpClient()

        request = requests.Request("GET", "http://localhost/")
        stub_request_with_response(request, "", 204)

        failed = False
        try:
            response = client.execute(request)
            self.assertIsNone(response.result)
        except BaseException:
            failed = True

        self.assertFalse(failed)

    @responses.activate
    def test_DefaultHttpClient_onSuccess_returnsResponse_with_invalid_json_body(self):
        client = DefaultHttpClient()

        request = requests.Request("GET", "http://localhost/")
        stub_request_with_response(request, "{\"some-invalid-json\": \"data\"}}}", 200)

        failed = False
        try:
            response = client.execute(request)
            self.assertEqual(response.result, "{\"some-invalid-json\": \"data\"}}}")
        except BaseException:
            failed = True

        self.assertFalse(failed)

    @responses.activate
    def test_DefaultHttpClient_onSuccess_returnsResponse_with_valid_json_body(self):
        client = DefaultHttpClient()

        request = requests.Request("GET", "http://localhost/")
        stub_request_with_response(request, "{\"valid_key\": \"valid-data\"}", 201)

        failed = False
        try:
            response = client.execute(request)
            self.assertEqual(response.result.valid_key, "valid-data")
        except BaseException:
            failed = True

        self.assertFalse(failed)

    @responses.activate
    def test_DefaultHttpClient_onSucces_escapesDashesWhenUnmarshaling(self):
        client = DefaultHttpClient()

        request = requests.Request("GET", "http://localhost/")
        stub_request_with_response(request, "{\"valid-key\": \"valid-data\"}", 201)

        failed = False
        try:
            response = client.execute(request)
            self.assertEqual(response.result.valid_key, "valid-data")
        except BaseException:
            failed = True

        self.assertFalse(failed)


if __name__ == '__main__':
    unittest.main()
