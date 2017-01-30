import requests
import base64
import http_client
import time


class AccessToken:
    def __init__(self, access_token, expires_in, token_type):
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.created_at = time.time()

    def is_expired(self):
        return self.created_at + self.expires_in <= time.time()


class RefreshToken:
    def __init__(self, refresh_token, access_token):
        self.refresh_token = refresh_token
        self.access_token = access_token


class TokenService:
    def __init__(self, environment):
        self.http_client = http_client.DefaultHttpClient()
        self.environment = environment

    def fetch_access_token(self, refresh_token=None):
        if refresh_token:
            return self._fetch_access_token_refresh_token(refresh_token)
        else:
            return self._fetch_access_token_client_id()

    def fetch_refresh_token(self, auth_code):
        request = self._get_access_token_request("/v1/identity/openidconnect/tokenservice")

        request.data = "grant_type=authorization_code&code=" + auth_code

        result = self.http_client.execute(request).result
        access_token = AccessToken(result.access_token, result.expires_in, result.token_type)

        return RefreshToken(result.refresh_token, access_token)

    def _fetch_access_token_refresh_token(self, refresh_token):
        request = self._get_access_token_request("/v1/identity/openidconnect/tokenservice")

        request.data = "grant_type=client_credentials&refresh_token=" + refresh_token

        result = self.http_client.execute(request).result

        return AccessToken(result.access_token, result.expires_in, result.token_type)

    def _fetch_access_token_client_id(self):
        request = self._get_access_token_request("/v1/oauth2/token")

        request.data = "grant_type=client_credentials"

        result = self.http_client.execute(request).result

        return AccessToken(result.access_token, result.expires_in, result.token_type)

    def _get_access_token_request(self, path):
        request = requests.Request(method="POST", url=self.environment.base_url + path)
        auth_header = base64.b64encode(self.environment.client_id + ":" + self.environment.client_secret)
        request.headers["Authorization"] = "Basic " + auth_header
        request.headers["Content-Type"] = "application/x-www-form-urlencoded"

        return request
