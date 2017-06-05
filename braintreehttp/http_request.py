
class HttpRequest(object):

    def __init__(self, path, verb, request_body=None):
        self.path = path
        self.verb = verb
        self.request_body = request_body
        self.headers = {}

    def header(self, key, value):
        self.headers[key] = value