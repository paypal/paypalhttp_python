import responses
import json
from core import *

OAUTH_PATH = "/v1/oauth2/token"
OPENID_CONNECT_PATH = "/v1/identity/openidconnect/tokenservice"


def stub_request_with_empty_reponse(request):
    stub_request_with_response(request, "{}", 200)


def stub_request_with_response(request, json, status):
    responses.add(request.method, request.url, body=json, content_type="application/json", status=status)


def stub_access_token_request(access_token_json=None):
    if not access_token_json:
        access_token_json = access_token_response()

    responses.add("POST", "http://localhost/v1/oauth2/token", body=access_token_json, status=200)


def access_token_request(refresh_token=None):
    url = "http://localhost"
    if refresh_token:
        url += "/v1/identity/openidconnect/tokenservice"
    else:
        url += "/v1/oauth2/token"
    return requests.Request(method="POST", url=url)


def access_token_response(refresh_token=None):
    resp = {
        "access_token": "sample-access-token",
        "expires_in": 3600,
        "token_type": "Bearer"
    }
    if refresh_token:
        resp["refresh_token"] = refresh_token

    return json.dumps(resp)
