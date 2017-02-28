import responses

def stub_request_with_empty_reponse(request):
    stub_request_with_response(request, "{}", 200)


def stub_request_with_response(request, json, status):
    responses.add(request.method, request.url, body=json, content_type="application/json", status=status)


