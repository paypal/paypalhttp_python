import requests
import time
import os

from braintreehttp.injector import Injector
from braintreehttp.encoder import Encoder
from braintreehttp.http_response import HttpResponse
from braintreehttp.http_exception import HttpException

LINE_FEED = "\r\n"

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
        if hasattr(request, 'body'):
            body = request.body
            if (isinstance(body, str)):
                data = body
            elif "Content-Type" in request.headers and "multipart/" in request.headers["Content-Type"]:
                boundary = str(time.time()).replace(".", "")
                request.headers["Content-Type"] = "multipart/form-data; boundary=" + boundary

                form_params = []
                for k, v in request.body.items():
                    if hasattr(v, "read"):  # It's a file
                        form_params.append(self.add_file_part(k, v))
                    else:                   # It's a regular form param
                        form_params.append(self.add_form_field(k, v))
                data = "--" + boundary + LINE_FEED + ("--" + boundary + LINE_FEED).join(form_params) + LINE_FEED + "--" + boundary + "--"
            else:
                data = self.serialize_request(request)

        resp = requests.request(method=request.verb,
                url=self.environment.base_url() + request.path,
                headers=request.headers,
                data=data)

        return self.parse_response(resp)

    def add_form_field(self, key, value):
        return "Content-Disposition: form-data; name=\"{}\"{}{}{}{}".format(key, LINE_FEED, LINE_FEED, value, LINE_FEED)

    def add_file_part(self, key, f):
        mime_type = self.mime_type_for_filename(os.path.basename(f.name))
        s = "Content-Disposition: form-data; name=\"{}\"; filename=\"{}\"{}".format(key, os.path.basename(f.name), LINE_FEED)
        return s + "Content-Type: {}{}{}{}{}".format(mime_type, LINE_FEED, LINE_FEED, f.read(), LINE_FEED)

    def mime_type_for_filename(self, filename):
        _, extension = os.path.splitext(filename)
        if extension == "jpeg" or extension == "jpg":
            return "image/jpeg"
        elif extension == "png":
            return "image/png"
        elif extension == "pdf":
            return "application/pdf"
        else:
            return "application/octet-stream"

    def serialize_request(self, request):
        return self.encoder.serialize_request(request)

    def deserialize_response(self, response_body, headers):
        return self.encoder.deserialize_response(response_body, headers)

    def parse_response(self, response):
        status_code = response.status_code

        if 200 <= status_code <= 299:
            body = ""
            if response.text and (len(response.text) > 0 and response.text != 'None'):
                body = self.deserialize_response(response.text, response.headers)

            return HttpResponse(body, response.status_code, response.headers)
        else:
            raise HttpException(response.text, response.status_code, response.headers)


