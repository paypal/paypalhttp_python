import requests
import injector as inj
from http_response import HttpResponse
from http_exeption import HttpException


class HttpClient(object):

    def __init__(self, environment):
        self._injectors = []
        self.environment = environment

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

        data = None
        if request.request_body is not None:
            if isinstance(request.request_body, str):
                data = request.request_body
            else:
                data = self.serialize_request(request)

        resp = requests.request(method=request.verb,
                                url=self.environment.base_url() + request.path,
                                headers=request.headers,
                                data=data)

        return self.parse_response(resp)

    def serialize_request(self, request):
        raise NotImplementedError

    def deserialize_response(self, response_body, headers):
        raise NotImplementedError

    def parse_response(self, response):
        status_code = response.status_code

        if 200 <= status_code <= 299:
            body = ""
            if response.text and (len(response.text) > 0 and response.text != 'None'):
                body = self.deserialize_response(response.text, response.headers)

            return HttpResponse(body, response.status_code, response.headers)
        else:
            raise HttpException(response.text, response.status_code, response.headers)


