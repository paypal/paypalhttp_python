import re
import os

class Encoder(object):

    def __init__(self, encoders):
        self.encoders = encoders

    def serialize_request(self, httprequest):
        if hasattr(httprequest, "headers"):
            if "content-type" in httprequest.headers:
                contenttype = httprequest.headers["content-type"]
                enc = self._encoder(contenttype)
                if enc:
                    return enc.encode(httprequest)
                else:
                    message = "Unable to serialize request with Content-Type {0}. Supported encodings are {1}".format(
                        contenttype, self.supported_encodings())
                    print(message)
                    raise IOError(message)
        else:
            message = "Http request does not have content-type header set"
            print(message)
            raise IOError(message)

    def deserialize_response(self, response_body, headers):
        if headers and "content-type" in headers:
            contenttype = headers["content-type"]
            enc = self._encoder(contenttype)
            if enc:
                return enc.decode(response_body)
            else:
                message = "Unable to deserialize response with content-type {0}. Supported decodings are {1}".format(
                    contenttype, self.supported_encodings())
                print(message)
                raise IOError(message)
        else:
            message = "Http response does not have content-type header set"
            print(message)
            raise IOError(message)


    def supported_encodings(self):
        return [enc.content_type() for enc in self.encoders]

    def _encoder(self, content_type):
        for enc in self.encoders:
            if re.match(enc.content_type(), content_type) is not None:
                return enc
        return None




