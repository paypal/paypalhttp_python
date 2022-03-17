import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, AnyStr, Dict, Iterable, Optional, Text, Tuple, Union

from paypalhttp.http_backends import AbstractBackend, Response

class MockBackend(AbstractBackend):
    def request(
        self,
        method,  # type: Text
        url,  # type: Text
        headers,  # type: Dict[Text, Text]
        data=None  # type: Optional[Union[AnyStr, Dict[Text, Any], Iterable[Tuple[Text, Any]]]]
    ):  # type: (...) -> Response
        return Response(
            status_code=200,
            text=json.dumps({'url': url, 'method': method}),
            headers={
                'server': 'MockBackend/1.0',
                'content-type': 'application/json',
            }
        )
