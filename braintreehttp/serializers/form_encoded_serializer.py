try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

class FormEncoded:
    def encode(self, request):
        params = []
        for k, v in request.body.items():
            params.append("{0}={1}".format(k, quote(v)))

        return '&'.join(params)

    def decode(self, data):
        raise IOError("FormEncoded does not support deserialization")

    def content_type(self):
        return "application/x-www-form-urlencoded"
