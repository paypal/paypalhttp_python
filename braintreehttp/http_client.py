import requests

from braintreehttp.injector import Injector
from braintreehttp.http_response import HttpResponse
from braintreehttp.http_exception import HttpException

class HttpClient(object):

    def __init__(self, environment):
        self._injectors = []
        self.environment = environment

    def get_user_agent(self):
        return "Python HTTP/1.1"

    def get_timeout(self):
        return 30

    def add_injector(self, injector):
        if injector and isinstance(injector, Injector):
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
        files = None
        try:
            body = getattr(request, 'body')

            if "Content-Type" in request.headers and "multipart/" in request.headers["Content-Type"]:
                files = {}
                filtered_body = {}
                for k in body:
                    v = body[k]
                    if hasattr(v, 'read'):
                        files[k] = v
                    else:
                        filtered_body[k] = v

                body = filtered_body

            # `requests` will multipart/form-data encode all data if a file is present
            if (files and len(files) > 0) or isinstance(body, str):
                data = body
            else:
                data = self.serialize_request(request)

        except AttributeError:
            pass

        resp = requests.request(method=request.verb,
                url=self.environment.base_url() + request.path,
                headers=request.headers,
                data=data,
                files=files)

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


