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

        formatted_headers = self.format_headers(reqCpy.headers)

        if "user-agent" not in formatted_headers:
            reqCpy.headers["user-agent"] = self.get_user_agent()

        if hasattr(reqCpy, 'body') and reqCpy.body is not None:
            raw_headers = reqCpy.headers
            reqCpy.headers = formatted_headers
            data = self.encoder.serialize_request(reqCpy)
            reqCpy.headers = self.map_headers(raw_headers, formatted_headers)

        resp = requests.request(method=reqCpy.verb,
                                url=self.environment.base_url + reqCpy.path,
                                headers=reqCpy.headers,
                                data=data)

        return self.parse_response(resp)

    def format_headers(self, headers):
        return dict((k.lower(), v) for k, v in headers.items())

    def map_headers(self, raw_headers, formatted_headers):
        for header_name in raw_headers:
            if header_name.lower() in formatted_headers:
                raw_headers[header_name] = formatted_headers[header_name.lower()]
        return raw_headers

    def parse_response(self, response):
        status_code = response.status_code

        if 200 <= status_code <= 299:
            body = ""
            if response.text and (len(response.text) > 0 and response.text != 'None'):
                body = self.encoder.deserialize_response(response.text, self.format_headers(response.headers))

            return HttpResponse(body, response.status_code, response.headers)
        else:
            raise HttpError(response.text, response.status_code, response.headers)
