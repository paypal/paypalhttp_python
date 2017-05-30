import requests
import injector as inj
from http_response import HttpResponse


class HttpClient(object):

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
                                json=request.json,)

        return self.parse_response(resp)

    def parse_response_body(self, response):
        return response.text

    def parse_response(self, response):
        status_code = response.status_code

        body = None
        if response.text and len(response.text) > 0:
            body = self.parse_response_body(response)

        if 200 <= status_code <= 299:
            return HttpResponse(response.status_code, response.headers, body)
        else:
            error_class = "APIException"

        data = {
            "status_code": status_code,
            "data": body,
            "headers": response.headers
        }

        if error_class:
            raise HttpResponse.construct_object(error_class, data, cls=IOError)


