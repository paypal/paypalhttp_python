import requests
import copy

from paypalhttp.encoder import Encoder
from paypalhttp.http_response import HttpResponse
from paypalhttp.http_error import HttpError
from paypalhttp.serializers import Json, Text, Multipart, FormEncoded

class HttpClient(object):

    def __init__(self, environment):
        self._injectors = []
        self.environment = environment
        self.encoder = Encoder([Json(), Text(), Multipart(), FormEncoded()])

    def get_user_agent(self):
        return "Python HTTP/1.1"

    def get_timeout(self):
        return 30

    def add_injector(self, injector):
        if injector and '__call__' in dir(injector):
            self._injectors.append(injector)
        else:
            message = "injector must be a function or implement the __call__ method"
            print(message)
            raise TypeError(message)

    def execute(self, request):
        reqCpy = copy.deepcopy(request)

        try:
            getattr(reqCpy, 'headers')
        except AttributeError:
            reqCpy.headers = {}

        for injector in self._injectors:
            injector(reqCpy)

        data = None
        if hasattr(reqCpy, 'body') and reqCpy.body is not None:
            data = self.encoder.serialize_request(reqCpy)

        if "user-agent" not in reqCpy.headers:
            reqCpy.headers["user-agent"] = self.get_user_agent()

        resp = requests.request(method=reqCpy.verb,
                url=self.environment.base_url + reqCpy.path,
                headers=reqCpy.headers,
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


