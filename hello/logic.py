from azure.functions import HttpRequest, HttpResponse

from wrappers import http
from errors import ValidationError


@http(template="hello/template.html")
def main(req: HttpRequest):
    if req.params.get('name') is None:
        raise ValidationError("Request worked, but you didn't give me a name!")
    if len(req.params) > 1:
        raise ValidationError("Request worked, but you gave me too many params!")
    
    return req.params


# -----------------------------------------------------------------------------
# For local calls

if __name__ == "__main__":
    # Run a test and output the result
    test_request = HttpRequest('GET', 'url', params={"name": "Test"}, body=bytes())
    r = main(test_request)  # type: ignore
    print(r.status_code, ":", r.get_body().decode("utf-8"))