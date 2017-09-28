import requests

from braintreehttp.encoder import Encoder
from braintreehttp.http_response import HttpResponse
from braintreehttp.http_error import HttpError


class HttpClient(object):

    def __init__(self, environment):
        self._injectors = []
        self.environment = environment
        self.encoder = Encoder()

    def get_user_agent(self):
        return "Python HTTP/1.1"

    def get_timeout(self):
        return 30

    def add_injector(self, injector):
        if injector and '__call__' in dir(injector):
            self._injectors.append(injector)
        else:
            raise TypeError("injector must be a function or implement the __call__ method")

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
        if hasattr(request, 'body') and request.body is not None:
            data = self.encoder.serialize_request(request)

        resp = requests.request(method=request.verb,
                url=self.environment.base_url + request.path,
                headers=request.headers,
                data=data)

        return self.parse_response(resp)

    def parse_response(self, response):
        status_code = response.status_code

        if 200 <= status_code <= 299:
            body = ""
            if response.text and (len(response.text) > 0 and response.text != 'None'):
                body = self.encoder.deserialize_response(response.text, response.headers)

            return HttpResponse(body, response.status_code, response.headers)
        else:
            raise HttpError(response.text, response.status_code, response.headers)


