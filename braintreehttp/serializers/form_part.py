class FormPart(object):

    def __init__(self, value, headers):
        self.value = value
        self.headers = {}

        for key in headers:
            self.headers['-'.join(map(lambda word: word[0].upper() + word[1:], key.lower().split('-')))] = headers[key]
