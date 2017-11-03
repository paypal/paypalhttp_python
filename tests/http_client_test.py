import unittest
import os
import responses

from braintreehttp import HttpClient
from braintreehttp.testutils import TestHarness


class GenericRequest:

    def __init__(self):
        self.path = ""
        self.verb = ""
        self.headers = {}

    def __str__(self):
        s = ""
        for key in dir(self):
            if not key.startswith("__"):
                s += "{0}: {1}\n".format(key, getattr(self, key))
        return s


class HttpClientTest(TestHarness):

    @responses.activate
    def test_HttpClient_execute_addsHeaders(self):
        client = HttpClient(self.environment())
        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"
        self.stub_request_with_empty_reponse(request)

        client.execute(request)

        call = responses.calls[0].request
        self.assertEqual(call.headers["User-Agent"], client.get_user_agent())

    def testHttpClient_addInjector_throwsWhenArgumentNotFunctional(self):
        client = HttpClient(self.environment())

        try:
            client.add_injector(1)
            self.fail("client.add_injector did not throw for non-functional argument")
        except TypeError as e:
            self.assertEqual(str(e), "injector must be a function or implement the __call__ method")

    @responses.activate
    def test_HttpClient_addInjector_usesInjectorClass(self):
        client = HttpClient(self.environment())

        class TestInjector():
            def __call__(self, request):
                request.headers["Foo"] = "Bar"

        client.add_injector(TestInjector())

        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"

        self.stub_request_with_empty_reponse(request)

        client.execute(request)

        call = responses.calls[0].request
        self.assertEqual(call.headers["Foo"], "Bar")

    @responses.activate
    def test_HttpClient_addInjector_usesInjectorFunction(self):
        client = HttpClient(self.environment())

        def inj(request):
            request.headers["Foo"] = "Bar"

        client.add_injector(inj)

        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"

        self.stub_request_with_empty_reponse(request)

        client.execute(request)

        call = responses.calls[0].request
        self.assertEqual(call.headers["Foo"], "Bar")

    @responses.activate
    def test_HttpClient_addInjector_usesInjectorLambda(self):
        client = HttpClient(self.environment())

        client.add_injector(lambda req: req.headers.clear())

        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"
        request.headers = {"Foo": "Bar"}

        self.stub_request_with_empty_reponse(request)

        client.execute(request)

        call = responses.calls[0].request
        self.assertFalse("Foo" in call.headers)

    @responses.activate
    def test_HttpClient_execute_usesAllParamsInRequest_plaintextdata(self):
        client = HttpClient(self.environment())
        request = GenericRequest()
        request.path = "/"
        request.verb = "POST"
        request.headers = {
                "Test": "Header",
                "Content-Type": "text/plain"
                }
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
        request.headers = {
                "Test": "Header",
                "Content-Type": "application/json"
                }
        request.body = {"some": "data"}

        self.stub_request_with_empty_reponse(request)

        client.execute(request)

        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0].request
        self.assertEqual(call.method, "POST")
        self.assertEqual(call.url, "http://localhost/")
        self.assertEqual(call.headers["Test"], "Header")
        self.assertEqual(call.body, "{\"some\": \"data\"}")

    @responses.activate
    def test_HttpClient_onError_throwsHttpErrorForNon200StatusCode(self):
        client = HttpClient(self.environment())

        request = GenericRequest()
        request.path = "/error"
        request.verb = "POST"
        self.stub_request_with_response(request, status=400, response_body="An error occurred!")

        try:
            client.execute(request)
        except BaseException as e:
            self.assertEqual("HttpError", e.__class__.__name__)
            self.assertEqual("An error occurred!", str(e))

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
    def test_HttpClient_parsesJSONArrayResponse(self):
        client = HttpClient(self.environment())

        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"

        response_body = '["one", "two"]'
        self.stub_request_with_response(request, response_body=response_body)

        resp = client.execute(request)

        self.assertEqual(resp.result, ["one", "two"])

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
    def test_HttpClient_executeDoesNotModifyRequest(self):
        client = HttpClient(self.environment())

        request = GenericRequest()
        request.path = "/"
        request.verb = "GET"
        self.stub_request_with_response(request, "{\"valid-key\": \"valid-data\"}", 201)

        client.execute(request)

        self.assertEquals(len(request.headers), 0)


if __name__ == '__main__':
    unittest.main()
