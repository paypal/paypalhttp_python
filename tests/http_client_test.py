import unittest
import os
import responses

from braintreehttp import HttpClient, Injector
from braintreehttp.testutils import TestHarness


class GenericRequest:
    pass


class HttpClientTest(TestHarness):

    @responses.activate
    def test_HttpClient_execute_addsHeaders(self):
        client = HttpClient(self.environment())
        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"
        self.stub_request_with_empty_reponse(request)

        client.execute(request)
        self.assertEqual(request.headers["User-Agent"], client.get_user_agent())

    @responses.activate
    def test_HttpClient_addInjector_usesInjector(self):
        client = HttpClient(self.environment())

        class TestInjector(Injector):
            def __call__(self, request):
                request.headers["Foo"] = "Bar"

        client.add_injector(TestInjector())

        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"

        self.stub_request_with_empty_reponse(request)

        client.execute(request)
        self.assertEqual(request.headers["Foo"], "Bar")

    @responses.activate
    def test_HttpClient_execute_usesAllParamsInRequest_plaintextdata(self):
        client = HttpClient(self.environment())
        request = GenericRequest()
        request.path = "/"
        request.verb = "POST"
        request.headers = {"Test": "Header"}
        request.body = "Some data"
        self.stub_request_with_empty_reponse(request)

        client.execute(request)

        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0].request
        self.assertEqual(call.method, "POST")
        self.assertEqual(call.url, "http://localhost/")
        self.assertEqual(call.headers["Test"], "Header")
        self.assertEqual(call.body, "Some data")

    @responses.activate
    def test_HttpClient_execute_usesAllParamsInRequest_json(self):
        client = HttpClient(self.environment())
        request = GenericRequest()
        request.path = "/"
        request.verb = "POST"
        request.headers = {"Test": "Header"}
        request.body = "{\"some\": \"data\"}"

        self.stub_request_with_empty_reponse(request)

        client.execute(request)

        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0].request
        self.assertEqual(call.method, "POST")
        self.assertEqual(call.url, "http://localhost/")
        self.assertEqual(call.headers["Test"], "Header")
        self.assertEqual(call.body, "{\"some\": \"data\"}")

    @responses.activate
    def test_HttpClient_onError_throwsHttpExceptionForNon200StatusCode(self):
        client = HttpClient(self.environment())

        request = GenericRequest()
        request.path = "/error"
        request.verb = "POST"
        self.stub_request_with_response(request, status=400, response_body="An error occurred!")

        try:
            client.execute(request)
        except BaseException as e:
            self.assertEqual("HttpException", e.__class__.__name__)
            self.assertEqual("An error occurred!", e.message)

    @responses.activate
    def test_HttpClient_onSuccess_returnsResponse_with_empty_body(self):
        client = HttpClient(self.environment())

        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"
        self.stub_request_with_response(request, status=204)

        response = client.execute(request)
        self.assertIsNone(response.result)

    @responses.activate
    def test_HttpClient_onSuccess_callsDeserializeResponse(self):

        class DeserializingHttpClient(HttpClient):
            def deserialize_response(self, response_body, headers):
                return "Some data"

            def serialize_request(self, request):
                return request.request_body

        client = DeserializingHttpClient(self.environment())

        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"
        self.stub_request_with_response(request, response_body="not some data", status=201)

        try:
            response = client.execute(request)
            self.assertEqual(response.result, "Some data")
        except BaseException as exception:
            self.fail(exception.message)

    @responses.activate
    def test_HttpClient_whenRequestBodyNotNone_callsSerializeRequest(self):

        class SerializingHttpClient(HttpClient):
            def deserialize_response(self, response_body, headers):
                return response_body

            def serialize_request(self, request):
                return "Serialized request"

        client = SerializingHttpClient(self.environment())

        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"
        request.body = {}
        self.stub_request_with_response(request)

        client.execute(request)

        call = responses.calls[0].request
        self.assertEqual(call.body, "Serialized request")

    @responses.activate
    def test_HttpClient_onSuccess_escapesDashesWhenUnmarshaling(self):
        client = HttpClient(self.environment())

        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"
        self.stub_request_with_response(request, "{\"valid-key\": \"valid-data\"}", 201)

        try:
            response = client.execute(request)
            self.assertEqual(response.result.valid_key, "valid-data")
        except BaseException as exception:
            self.fail(exception.message)

    @responses.activate
    def test_HttpClient_setsFileWhenPresent(self):
        client = HttpClient(self.environment())

        request = GenericRequest()
        request.path = "/"
        request.verb = "POST"
        request.headers = {"Content-Type": "multipart/form-data"}
        request.body = {'file': open(abspath('./README.md'), 'rb')}

        self.stub_request_with_response(request)
        client.execute(request)

        call = responses.calls[0].request
        self.assertTrue(b"README" in call.body)
        self.assertTrue(b"Content-Disposition: form-data" in call.body)

    @responses.activate
    def test_HttpClient_setsDataWhenFilePresent(self):
        client = HttpClient(self.environment())

        request = GenericRequest()
        request.path = "/"
        request.verb = "POST"
        request.headers = {"Content-Type": "multipart/form-data"}
        request.body = {"some_key": "some_value", "some_nested[key]": "some_nested_value", "file": open(abspath('README.md'), 'rb')}

        self.stub_request_with_response(request)
        client.execute(request)

        call = responses.calls[0].request

        self.assertTrue(b"Content-Disposition: form-data; name=\"some_key\"" in call.body)
        self.assertTrue(b"some_value" in call.body)
        self.assertTrue(b"Content-Disposition: form-data; name=\"some_nested[key]\"" in call.body)
        self.assertTrue(b"some_nested_value" in call.body)
        self.assertTrue(b"Content-Disposition: form-data; name=\"file\"; filename=\"README.md\"" in call.body)

def abspath(path):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), path)

if __name__ == '__main__':
    unittest.main()
