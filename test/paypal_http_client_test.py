import unittest
from unit_test_utils import *

env = Environment("clientId", "clientSecret", "http://localhost")


class PayPalHttpClientTest(unittest.TestCase):
    def setUp(self):
        self.request = requests.Request(method="GET", url="http://localhost/")
        stub_request_with_empty_reponse(self.request)
        self.client = PayPalHttpClient(env)
        stub_access_token_request()

    @responses.activate
    def testPayPalHttpClient_execute_setsCommonHeaders_and_signsRequest(self):
        self.client.execute(self.request)

        self.assertEqual(len(responses.calls), 2)
        self.assertEquals(self.request.headers["Accept-Encoding"], "gzip")
        self.assertEquals(responses.calls[1].request.headers["Authorization"], "Bearer sample-access-token")

    @responses.activate
    def testPayPalHttpClient_execute_setsContentTypeHeaderWhenRequestBodyPresent(self):
        self.request.json = {"some": "json"}
        self.client.execute(self.request)

        self.assertEqual(len(responses.calls), 2)
        self.assertEquals(self.request.headers["Content-Type"], "application/json")

    @responses.activate
    def testPayPalHttpClient_execute_setsBaseUrl(self):
        self.request = requests.Request(method="GET", url="/special")

        stub_request_with_empty_reponse(requests.Request(method="GET", url=env.base_url + "/special"))
        self.client.execute(self.request)

        self.assertEqual(len(responses.calls), 2)
        self.assertTrue(self.request.url.startswith(env.base_url))


if __name__ == '__main__':
    unittest.main()
