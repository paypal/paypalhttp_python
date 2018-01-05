## Braintree HttpClient [![Build Status](https://travis-ci.org/braintree/braintreehttp_python.svg?branch=master)](https://travis-ci.org/braintree/braintreehttp_python)

BraintreeHttp is a generic HTTP Client.

In it's simplest form, an [`HttpClient`](./braintreehttp/http_client.py) exposes an `#execute` method which takes an HTTP request, executes it against the domain described in an `Environment`, and returns an `HttpResponse`. It throws an Error, and potentially an HttpError, if anything goes wrong during execution.

### Environment

An [`Environment`](./braintreehttp/environment.py) describes a domain that hosts a REST API, against which an `HttpClient` will make requests. `Environment` is a simple class that contains one property, `base_url`.

```py
env = Environment("https://example.com")
```

### Requests

HTTP request objects contain all the information needed to make an HTTP request against the REST API. Specifically, one request object describes a path, a verb, any path/query/form parameters, headers, attached files for upload, and body data.

### Responses

[`HttpResponse`](./braintreehttp/http_response.py)s contain information returned by a server in response to a request as described above. They contain a `status_code`, `headers`, and a `result`, which represents any data returned by the server.

```py
class GenericRequest():
  def __init__(self):
    self.path = "/path/to/resource"
    self.verb = "GET"
    self.headers = {
      "X-Custom-Header": "custom value"
    }

resp = client.execute(GenericRequest())
```

### Injectors

Injectors are functions that can be used for executing arbitrary pre-flight logic, such as modifying a request or logging data. Injectors are attached to an `HttpClient` using the `#add_injector` method. They may take the form of a class that implements `__call__`, a function reference, or a lambda expression.

The HttpClient executes its `Injector`s in a first-in, first-out order, before each request.

```py
client = HttpClient(env)

class HeadersInjector():
  def __call__(req):
    req.headers["Request-Id"] = "abcd"

client.add_injector(HeadersInjector())

def inject_query_param(req):
  req.path += "?query=param"

client.add_injector(inject_query_param)

client.add_injector(lambda req: print req)

...
```

### Error Handling

`HttpClient#execute` may raise an `IOError` if something went wrong during the course of execution. If the server returned a non-200 response, this execption will be an instance of [`HttpError`](./braintreehttp/http_error.py) that will contain a status code and headers you can use for debugging. 

```py
try:
  resp = client.execute(req)
  status_code = resp.status_code
  headers = resp.headers
  response_data = resp.result
except IOError as ioe:
  if isinstance(ioe, HttpException):
    # Inspect this exception for details
    status_code = ioe.status_code
    headers = ioe.headers
    message = str(ioe)
  else:
    # Something else went wrong
    print ioe
```

### Serializer
(De)Serialization of request and response data is done by instances of [`Encoder`](./braintreehttp/encoder.py). BraintreeHttp currently supports `json` encoding out of the box.

## License
BraintreeHttp-Python is open source and available under the MIT license. See the [LICENSE](./LICENSE) file for more info.

## Contributing
Pull requests and issues are welcome. Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for more details.
