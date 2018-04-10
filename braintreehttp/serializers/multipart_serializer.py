import time
import os

from braintreehttp import  File
from braintreehttp.encoder import Encoder
from braintreehttp.serializers.form_part import FormPart

from braintreehttp.serializers import Json, Text, FormEncoded

CRLF = "\r\n"

class FormPartRequest:
    pass

class Multipart:

    def encode(self, request):
        boundary = str(time.time()).replace(".", "")
        request.headers["Content-Type"] = "multipart/form-data; boundary=" + boundary

        params = []
        form_params = []
        file_params = []
        for k, v in request.body.items():
            if isinstance(v, File):
                file_params.append(self.add_file_part(k, v))
            elif isinstance(v, FormPart):
                form_params.append(self.add_form_part(k, v))
            else:                   # It's a regular form param
                form_params.append(self.add_form_field(k, v))

        params = form_params + file_params
        data = "--" + boundary + CRLF + ("--" + boundary + CRLF).join(params) + CRLF + "--" + boundary + "--"

        return data

    def decode(self, data):
        raise IOError('Multipart does not support deserialization.')

    def content_type(self):
        return "multipart/.*"

    def add_form_field(self, key, value):
        return "Content-Disposition: form-data; name=\"{}\"{}{}{}{}".format(key, CRLF, CRLF, value, CRLF)

    def add_form_part(self, key, formPart):
        retValue =  "Content-Disposition: form-data; name=\"{}\"".format(key)
        if formPart.headers["Content-Type"] == "application/json":
            retValue += "; filename=\"{}.json\"".format(key)
        retValue += CRLF

        for key in formPart.headers:
            retValue += "{}: {}{}".format(key, formPart.headers[key], CRLF)

        retValue += CRLF

        req = FormPartRequest()
        req.headers = formPart.headers
        req.body = formPart.value
        retValue += Encoder([Json(), Text(), FormEncoded()]).serialize_request(req)

        retValue += CRLF
        return retValue

    def add_file_part(self, key, f):
        mime_type = self.mime_type_for_filename(os.path.basename(f.name))
        s = "Content-Disposition: form-data; name=\"{}\"; filename=\"{}\"{}".format(key, os.path.basename(f.name), CRLF)
        return s + "Content-Type: {}{}{}{}{}".format(mime_type, CRLF, CRLF, f.read(), CRLF)

    def mime_type_for_filename(self, filename):
        _, extension = os.path.splitext(filename)
        if extension == ".jpeg" or extension == ".jpg":
            return "image/jpeg"
        elif extension == ".png":
            return "image/png"
        elif extension == ".gif":
            return "image/gif"
        elif extension == ".pdf":
            return "application/pdf"
        else:
            return "application/octet-stream"
