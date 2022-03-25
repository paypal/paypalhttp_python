from collections import namedtuple
from typing import Any, NamedTuple, TYPE_CHECKING, Dict, Text

if TYPE_CHECKING:
    from typing import AnyStr, Iterable, Optional, Tuple, Union

try:
    import requests
except ImportError:
    requests = None


"""
Local replacement for requests.Response.
"""
Response = NamedTuple(
    "Response",
    [
        ('status_code', int),
        ('text', Text),
        ('headers', Dict[Text, Text]),
    ]
)

class AbstractBackend:
    """
    Function prototype for HTTP backends to perform requests.
    """
    def request(
        self,
        method,  # type: Text
        url,  # type: Text
        headers,  # type: Dict[Text, Text]
        data=None  # type: Optional[Union[AnyStr, Dict[Text, Any], Iterable[Tuple[Text, Any]]]]
    ):  # type: (...) -> Response
        raise NotImplementedError()


class RequestsBackend(AbstractBackend):
    def __init__(self, session=None):  # type: (Optional[requests.Session]) -> None
        if requests is None:
            raise RuntimeError(
                "requests is not available in your Python environment. Please install it "
                "using pip or your distribution's package manager."
            )

        if session is None:
            session = requests.Session()

        self.session = session

    def request(
        self,
        method,  # type: Text
        url,  # type: Text
        headers,  # type: Dict[Text, Text]
        data=None  # type: Optional[Union[AnyStr, Dict[Text, Any], Iterable[Tuple[Text, Any]]]]
    ):  # type: (...) -> Response
        resp = self.session.request(
            method=method,
            url=url,
            headers=headers,
            data=data
        )

        return Response(
            status_code=resp.status_code,
            text=resp.text,
            headers=resp.headers
        )
