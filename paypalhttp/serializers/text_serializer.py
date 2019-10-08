class Text:

    def encode(self, request):
        return str(request.body)

    def decode(self, data):
        return str(data)

    def content_type(self):
        return "text/.*"
