
class HttpException(IOError):

    def __init__(self, message, status_code, headers):
        IOError.__init__(self, message)
        self.status_code = status_code
        self.headers = headers
