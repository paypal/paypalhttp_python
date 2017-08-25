import json
import re
import os
import time

LINE_FEED = "\r\n"

class Encoder(object):

    def __init__(self):
        self.encoders = [Json(), Text(), Multipart()]

    def serialize_request(self, httprequest):
        if hasattr(httprequest, "headers") and "Content-Type" in httprequest.headers:
            contenttype = httprequest.headers["Content-Type"]
            enc = self._encoder(contenttype)
            if enc:
                return enc.encode(httprequest)
            else:
                raise IOError("Unable to serialize request with Content-Type {0}. Supported encodings are {1}".format(contenttype, self.supported_encodings()))
        else:
            raise IOError("Http request does not have Content-Type header set")

    def deserialize_response(self, response_body, headers):
        if headers and "Content-Type" in headers:
            contenttype = headers["Content-Type"]
            enc = self._encoder(contenttype)
            if enc:
                return enc.decode(response_body)
            else:
                raise IOError("Unable to deserialize response with Content-Type {0}. Supported decodings are {1}".format(contenttype, self.supported_encodings()))
        else:
            raise IOError("Http response does not have Content-Type header set")

    def supported_encodings(self):
        return [enc.content_type() for enc in self.encoders]

    def _encoder(self, content_type):
        for enc in self.encoders:
            if re.match(enc.content_type(), content_type) is not None:
                return enc
        return None

class Json:

    def encode(self, request):
        return json.dumps(request.body)

    def decode(self, data):
        return json.loads(data)

    def content_type(self):
        return "application/json"


class Text:

    def encode(self, request):
        return str(request.body)

    def decode(self, data):
        return str(data)

    def content_type(self):
        return "text/.*"


class Multipart:

    def encode(self, request):
        boundary = str(time.time()).replace(".", "")
        request.headers["Content-Type"] = "multipart/form-data; boundary=" + boundary

        form_params = []
        for k, v in request.body.items():
            if hasattr(v, "read"):  # It's a file
                form_params.append(self.add_file_part(k, v))
            else:                   # It's a regular form param
                form_params.append(self.add_form_field(k, v))
        data = "--" + boundary + LINE_FEED + ("--" + boundary + LINE_FEED).join(form_params) + LINE_FEED + "--" + boundary + "--"

        return data

    def decode(self, data):
        raise IOError('Multipart does not support deserialization.')

    def content_type(self):
        return "multipart/.*"

    def add_form_field(self, key, value):
        return "Content-Disposition: form-data; name=\"{}\"{}{}{}{}".format(key, LINE_FEED, LINE_FEED, value, LINE_FEED)

    def add_file_part(self, key, f):
        mime_type = self.mime_type_for_filename(os.path.basename(f.name))
        s = "Content-Disposition: form-data; name=\"{}\"; filename=\"{}\"{}".format(key, os.path.basename(f.name), LINE_FEED)
        return s + "Content-Type: {}{}{}{}{}".format(mime_type, LINE_FEED, LINE_FEED, f.read(), LINE_FEED)

    def mime_type_for_filename(self, filename):
        _, extension = os.path.splitext(filename)
        if extension == ".jpeg" or extension == ".jpg":
            return "image/jpeg"
        elif extension == ".png":
            return "image/png"
        elif extension == ".pdf":
            return "application/pdf"
        else:
            return "application/octet-stream"
