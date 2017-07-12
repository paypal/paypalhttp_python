import requests
import injector as inj
from http_response import HttpResponse
from http_exception import HttpException

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
        try:
            getattr(request, 'headers')
        except AttributeError:
            request.headers = {}

        for injector in self._injectors:
            injector(request)

        if "User-Agent" not in request.headers:
            request.headers["User-Agent"] = self.get_user_agent()

        data = None
        try:
            getattr(request, 'body')
        except AttributeError:
            pass
        else:
            if isinstance(request.body, str):
                data = request.body
            else:
                data = self.serialize_request(request)

        resp = requests.request(method=request.verb,
                url=self.environment.base_url() + request.path,
                headers=request.headers,
                data=data)

        return self.parse_response(resp)

    def serialize_request(self, request):
        return request.body

    def deserialize_response(self, response_body, headers):
        return response_body

    def parse_response(self, response):
        status_code = response.status_code

        if 200 <= status_code <= 299:
            body = ""
            if response.text and (len(response.text) > 0 and response.text != 'None'):
                body = self.deserialize_response(response.text, response.headers)

            return HttpResponse(body, response.status_code, response.headers)
        else:
            raise HttpException(response.text, response.status_code, response.headers)


