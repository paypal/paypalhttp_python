import unittest
from unit_test_utils import *

env = Environment("clientId", "clientSecret", "http://localhost")


class TokenServiceTest(unittest.TestCase):
    @responses.activate
    def testTokenService_fetchAccessToken_clientId_fetchesAccessToken(self):
        token_service = TokenService(env)

        stub_request_with_response(token_service._get_access_token_request(OAUTH_PATH), status=200,
                                   json=access_token_response())

        token_service.fetch_access_token()

        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0].request
        self.assertTrue(call.url.endswith(OAUTH_PATH))
        self.assertTrue(call.headers["Authorization"].startswith("Basic "))
        self.assertEqual(call.headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(call.body, "grant_type=client_credentials")

    @responses.activate
    def testTokenService_fetchAccessToken_refreshToken_fetchesAccessToken(self):
        token_service = TokenService(env)

        stub_request_with_response(token_service._get_access_token_request(OPENID_CONNECT_PATH), status=200,
                                   json=access_token_response())

        token_service.fetch_access_token("refresh-token")

        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0].request
        self.assertTrue(call.url.endswith(OPENID_CONNECT_PATH))
        self.assertTrue(call.headers["Authorization"].startswith("Basic "))
        self.assertEqual(call.headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(call.body, "grant_type=client_credentials&refresh_token=refresh-token")

    @responses.activate
    def testTokenService_fetchesRefreshToken_and_deserializes(self):
        token_service = TokenService(env)

        stub_request_with_response(token_service._get_access_token_request(OPENID_CONNECT_PATH), status=200,
                                   json=access_token_response("fresh-refresh-token"))

        refresh_token = token_service.fetch_refresh_token("sample_authorization_code")

        self.assertEqual(len(responses.calls), 1)
        call = responses.calls[0].request
        self.assertTrue(call.url.endswith(OPENID_CONNECT_PATH))
        self.assertTrue(call.headers["Authorization"].startswith("Basic "))
        self.assertEqual(call.headers["Content-Type"], "application/x-www-form-urlencoded")
        self.assertEqual(call.body, "grant_type=authorization_code&code=sample_authorization_code")
        self.assertEqual(refresh_token.refresh_token, "fresh-refresh-token")
        self.assertEqual(refresh_token.access_token.access_token, "sample-access-token")
        self.assertEqual(refresh_token.access_token.token_type, "Bearer")
        self.assertEqual(refresh_token.access_token.expires_in, 3600)


if __name__ == '__main__':
    unittest.main()
