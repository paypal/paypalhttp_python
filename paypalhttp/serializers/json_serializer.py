import json


class Json:

    def encode(self, request):
        return json.dumps(request.body)

    def decode(self, data):
        return json.loads(data)

    def content_type(self):
        return "application/json"
