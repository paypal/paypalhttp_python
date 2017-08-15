import responses
import unittest
import json
import braintreehttp

class TestHarness(unittest.TestCase):

    def environment(self):
        return braintreehttp.Environment("http://localhost")

    def stub_request_with_empty_reponse(self, request):
        self.stub_request_with_response(request)


    def stub_request_with_response(self, request, response_body="", status=200, content_type="application/json"):
        body = None
        if response_body:
            if isinstance(response_body, str):
                body = response_body
            else:
                body = json.dumps(response_body)


        responses.add(request.verb, self.environment().base_url + request.path, body=body, content_type=content_type, status=status)


