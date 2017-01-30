import unittest
from unit_test_utils import *

env = Environment("clientId", "clientSecret", "http://localhost")


class AuthInjectorTest(unittest.TestCase):
    @responses.activate
    def testOAuthInjector_inject_fetchesAccessTokenIfExpired(self):
        injector = AuthInjector(env)
        injector.access_token = AccessToken("sample-access-token", 0, "Bearer")

        request = requests.Request(method="GET", url="http://localhost/")
        stub_request_with_response(injector.token_service._get_access_token_request(OAUTH_PATH), status=200,
                                   json=access_token_response())

        injector(request)

        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0].request
        self.assertTrue(call.url.endswith(OAUTH_PATH))

    @responses.activate
    def testOAuthInjector_inject_setsAuthorizationHeader(self):
        injector = AuthInjector(env)

        request = requests.Request(method="GET", url="http://localhost/")
        stub_request_with_response(injector.token_service._get_access_token_request(OAUTH_PATH), status=200,
                                   json=access_token_response())

        injector(request)

        self.assertEqual(request.headers["Authorization"], "Bearer sample-access-token")

    @responses.activate
    def test_OAuthInjector_clientId_inject_fetchesAccessTokenIfNotCached(self):
        injector = AuthInjector(env)

        request = requests.Request(method="GET", url="http://localhost/")
        stub_request_with_response(injector.token_service._get_access_token_request(OAUTH_PATH), status=200,
                                   json=access_token_response())

        injector(request)

        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0].request
        self.assertTrue(call.url.endswith(OAUTH_PATH))

    @responses.activate
    def testOAuthInjector_refreshToken_fetchesAccessTokenIfNotCached(self):
        injector = AuthInjector(env, "refresh_token")

        request = requests.Request(method="GET", url="http://localhost/")
        stub_request_with_response(injector.token_service._get_access_token_request(OPENID_CONNECT_PATH), status=200,
                                   json=access_token_response())

        injector(request)

        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0].request
        self.assertTrue(call.url.endswith(OPENID_CONNECT_PATH))


if __name__ == '__main__':
    unittest.main()
