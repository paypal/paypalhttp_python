import json


class Encoder(object):

    def __init__(self):
        self.encoders = {}

    def serialize_request(self, httprequest):
        if hasattr(httprequest, "headers") and "Content-Type" in httprequest.headers:
            contenttype = httprequest.headers["Content-Type"]
            if contenttype == "application/json":
                return json.dumps(httprequest.body)
            else:
                raise IOError("Unable to serialize request with Content-Type {0}. Supported encodings are {1}".format(contenttype, self.supported_encodings()))
        else:
            raise IOError("Http request does not have Content-Type header set")

    def deserialize_response(self, response_body, headers):
        if headers and "Content-Type" in headers:
            contenttype = headers["Content-Type"]
            if contenttype == "application/json":
                return json.loads(response_body)
            else:
                raise IOError("Unable to deserialize response with Content-Type {0}. Supported decodings are {1}".format(contenttype, self.supported_decodings()))
        else:
            raise IOError("Http response does not have Content-Type header set")

    def supported_encodings(self):
        return "[application/json]"

    def supported_decodings(self):
        return "[application/json]"

