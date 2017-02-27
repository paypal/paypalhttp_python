import requests
import injector as inj
from http_response import HttpResponse


class DefaultHttpClient(object):

    def __init__(self):
        self._injectors = []

    def get_user_agent(self):
        return "Python HTTP/1.1"

    def get_timeout(self):
        return 30

    def add_injector(self, injector):
        if injector and isinstance(injector, inj.Injector):
            self._injectors.append(injector)
        else:
            raise TypeError("injector must be an instance of Injector")

    def execute(self, request):
        for injector in self._injectors:
            injector(request)

        if "User-Agent" not in request.headers:
            request.headers["User-Agent"] = self.get_user_agent()

        resp = requests.request(method=request.method,
                                url=request.url,
                                headers=request.headers,
                                data=request.data,
                                auth=request.auth,
                                json=request.json, )

        return DefaultHttpClient.parse_response(resp)

    @staticmethod
    def parse_response(response):
        status_code = response.status_code

        body = str(response.text)
        try:
            body = response.json()
        except ValueError:
            pass  # body is either empty or isn't a json-formatted string

        error_class = None
        if 200 <= status_code <= 299:
            return HttpResponse(response.status_code, response.headers, body)
        elif status_code == 401:
            error_class = "AuthenticationError"
        elif status_code == 403:
            error_class = "AuthorizationError"
        elif status_code == 400:
            error_class = "BadRequestError"
        elif status_code == 404:
            error_class = "ResourceNotFoundError"
        elif status_code == 422:
            error_class = "UnprocessableEntityError"
        elif status_code == 426:
            error_class = "UpgradeRequiredError"
        elif status_code == 429:
            error_class = "RateLimitError"
        elif status_code == 500:
            error_class = "InternalServerError"
        elif status_code == 503:
            error_class = "DownForMaintenanceError"

        data = {
            "status_code": status_code,
            "data": body,
            "headers": response.headers
        }
        if error_class:
            raise HttpResponse.construct_object(error_class, data, cls=IOError)
        else:
            raise IOError(response.text)


