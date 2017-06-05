class HttpResponse(object):

    def __init__(self, data, status_code, headers=None):
        if headers is None:
            headers = {}

        self.status_code = status_code
        self.headers = headers
        if data and len(data) > 0:
            if isinstance(data, str):
                self.result = data
            elif isinstance(data, dict):
                self.result = HttpResponse.construct_object('Result', data)  # todo: pass through response type
        else:
            self.result = None

    @staticmethod
    def construct_object(name, data, cls=object):
        obj = type(str(name), (cls,), {})
        for k, v in data.iteritems():
            k = str(k).replace("-", "_").lower()
            if isinstance(v, dict):
                setattr(obj, k, HttpResponse.construct_object(k, v))
            elif isinstance(v, list):
                l = []
                for item in v:
                    l.append(HttpResponse.construct_object(k, item))
                setattr(obj, k, l)
            else:
                setattr(obj, k, v)

        return obj
