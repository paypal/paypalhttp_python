import requests
import injector


class HttpClient:

    def __init__(self):
        self._injectors = []

    def get_user_agent(self):
        return "Python HTTP/1.1"

    def get_timeout(self):
        return 30

    def add_injector(self, injector):
        if injector and isinstance(injector, injector.Injector):
            self._injectors.append(injector)
        else:
            raise TypeError("injector must be an instance of Injector")

    def execute(self, request):
        for injector in self._injectors:
            injector(request)

        if "User-Agent" not in request.headers:
            request.headers["User-Agent"] = self.get_user_agent()

        resp = requests.request(method=request.method,
                                url=request.url,
                                headers=request.headers,
                                data=request.data,
                                auth=request.auth,
                                json=request.json,)

        return HttpClient.parse_response(resp)

    @staticmethod
    def parse_response(response):
        status_code = response.status_code
        data = {
            "status_code": status_code,
            "data": response.json(),
            "headers": response.headers
        }

        error_class = None
        if 200 <= status_code <= 299:
            return HttpResponse(response.status_code, response.headers, response.json())
        elif status_code == 401:
            error_class = "AuthenticationError"
        elif status_code == 403:
            error_class = "AuthorizationError"
        elif status_code == 400:
            error_class = "BadRequestError"
        elif status_code == 404:
            error_class = "ResourceNotFoundError"
        elif status_code == 422:
            error_class = "UnprocessableEntityError"
        elif status_code == 426:
            error_class = "UpgradeRequiredError"
        elif status_code == 429:
            error_class = "RateLimitError"
        elif status_code == 500:
            error_class = "InternalServerError"
        elif status_code == 503:
            error_class = "DownForMaintenanceError"

        if error_class:
            raise _construct_object(error_class, data, cls=IOError)
        else:
            raise IOError(response.text)


class PayPalHttpClient(HttpClient):

    def __init__(self, environment, auth_injector=None):
        HttpClient.__init__(self)
        self.environment = environment
        if auth_injector:
            self.add_injector(auth_injector)
        else:
            auth_injector = injector.AuthInjector(environment)
            self.add_injector(auth_injector)

        self.add_injector(injector=PayPalHttpClient.PayPalDefaultInjector(environment.base_url))

    class PayPalDefaultInjector(injector.Injector):

        def __init__(self, base_url):
            self.base_url = base_url

        def __call__(self, request):
            if "http" not in request.url:
                request.url = self.base_url + request.url

            if request.json:
                request.headers["Content-Type"] = "application/json"

            if "Accept-Encoding" not in request.headers:
                request.headers["Accept-Encoding"] = "gzip"


class HttpResponse:

    def __init__(self, status_code, headers, data):
        self.status_code = status_code
        self.headers = headers
        if len(data) > 0:
            self.result = _construct_object('Result', data)
        else:
            self.result = None


def _construct_object(name, data, cls=object):
    obj = type(str(name), (cls,), data)
    for k, v in data.iteritems():
        if isinstance(v, dict):
            setattr(obj, str(k), _construct_object(str(k), v))
        elif isinstance(v, list):
            l = []
            for item in v:
                l.append(_construct_object(str(k), item))
            setattr(obj, str(k), l)

    return obj
