import re
import os

from braintreehttp.serializers import Json, Text, Multipart, FormEncoded


class Encoder(object):

    def __init__(self):
        self.encoders = [Json(), Text(), Multipart(), FormEncoded()]

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




