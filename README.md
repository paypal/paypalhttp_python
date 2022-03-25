## PayPal HttpClient 
PayPalHttp is a generic HTTP Client.

In it's simplest form, an [`HttpClient`](paypalhttp/http_client.py) exposes an `#execute` method which takes an HTTP request, executes it against the domain described in an `Environment`, and returns an `HttpResponse`. It throws an Error, and potentially an HttpError, if anything goes wrong during execution.

### Environment

An [`Environment`](paypalhttp/environment.py) describes a domain that hosts a REST API, against which an `HttpClient` will make requests. `Environment` is a simple class that contains one property, `base_url`.

```py
env = Environment("https://example.com")
```

### Requests

HTTP request objects contain all the information needed to make an HTTP request against the REST API. Specifically, one request object describes a path, a verb, any path/query/form parameters, headers, attached files for upload, and body data.

### Responses

[`HttpResponse`](paypalhttp/http_response.py)s contain information returned by a server in response to a request as described above. They contain a `status_code`, `headers`, and a `result`, which represents any data returned by the server.

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

### Backends

If you need even more control over the request, for example to route the request through custom proxying or rewriting logic, you can provide your own backend to `HttpClient` by implementing `paypalhttp.http_backends.AbstractBackend` and passing an instance of that implementation as the second argument (`backend=`) to the constructor of `HttpClient`.

The backend must implement one method, `#request`, accepting the following arguments:

* `method`: _(Text)_ The HTTP request method
* `url`: _(Text)_ The full URL that will be requested, including the prefix.
* `headers`: _(Dict[Text, Text])_ Headers to be set on the request.
* `data`: _(RequestsBody)_ The body of the request, for methods that support it. `RequestsBody` is defined as any one of the following:
  * `None`
  * `AnyStr` (`str` or `bytes` in Python 3; `str` or `unicode` in Python 2)
  * `Dict[Text, Any]` (`Text` is `str` in Python 3 and `unicode` in Python 2)
  * `Iterable[Tuple[Text, Any]]`

If an exception is not thrown, `#request` must return a `paypalhttp.http_backends.Response`, which is a `NamedTuple` with the following fields (all are required):

* `status_code`: `int`
* `text`: `Text`
* `headers`: `Dict[Text, Text]`

The included backend, `RequestsBackend`, relies on `requests`. While `requests` is listed in `requirements.txt`, it is not in fact required if you will always pass your own backend to `HttpClient`.

### Error Handling

`HttpClient#execute` may raise an `IOError` if something went wrong during the course of execution. If the server returned a non-200 response, this execption will be an instance of [`HttpError`](paypalhttp/http_error.py) that will contain a status code and headers you can use for debugging. 

```py
try:
  resp = client.execute(req)
  status_code = resp.status_code
  headers = resp.headers
  response_data = resp.result
except HttpError as err:
  # Inspect this exception for details
  status_code = err.status_code
  headers = err.headers
  message = str(err)
except IOError as ioe:
  # Something else went wrong
  print ioe
```

### Serializer
(De)Serialization of request and response data is done by instances of [`Encoder`](paypalhttp/encoder.py). PayPalHttp currently supports `json` encoding out of the box.

## License
PayPalHttp-Python is open source and available under the MIT license. See the [LICENSE](./LICENSE) file for more info.

## Contributing
Pull requests and issues are welcome. Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for more details.
