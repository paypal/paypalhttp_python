import time
import os


CRLF = "\r\n"


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
        data = "--" + boundary + CRLF + ("--" + boundary + CRLF).join(form_params) + CRLF + "--" + boundary + "--"

        return data

    def decode(self, data):
        raise IOError('Multipart does not support deserialization.')

    def content_type(self):
        return "multipart/.*"

    def add_form_field(self, key, value):
        return "Content-Disposition: form-data; name=\"{}\"{}{}{}{}".format(key, CRLF, CRLF, value, CRLF)

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
        elif extension == ".pdf":
            return "application/pdf"
        else:
            return "application/octet-stream"
