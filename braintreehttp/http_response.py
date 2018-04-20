def setattr_mixed(dest, key, value):
    if isinstance(dest, list):
        dest.append(value)
    else:
        setattr(dest, key, value)


def construct_object(name, data, cls=object):
    if isinstance(data, dict):
        iterator = iter(data)
        dest = Result(data)
    elif isinstance(data, list):
        iterator = range(len(data))
        dest = []
    else:
        return data

    for k in iterator:
        v = data[k]

        k = str(k).replace("-", "_").lower()
        if isinstance(v, dict):
            setattr_mixed(dest, k, construct_object(k, v))
        elif isinstance(v, list):
            l = []
            for i in range(len(v)):
                setattr_mixed(l, i, construct_object(k, v[i]))

            setattr_mixed(dest, k, l)
        else:
            setattr_mixed(dest, k, v)

    return dest


class Result(object):

    def __init__(self, data):
        self._dict = data;

    def dict(self):
        return self._dict

    def __contains__(self, key):
        return key in self._dict

    def __getitem__(self, key):
        return self._dict[key]


class HttpResponse(object):

    def __init__(self, data, status_code, headers=None):
        if headers is None:
            headers = {}

        self.status_code = status_code
        self.headers = headers
        if data and len(data) > 0:
            if isinstance(data, str):
                self.result = data
            elif isinstance(data, dict) or isinstance(data, list):
                self.result = construct_object('Result', data)  # todo: pass through response type
        else:
            self.result = None

