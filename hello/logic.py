from wrappers import http
from errors import ValidationError

from azure.functions import HttpRequest


@http(template="hello/template.html")
def main(req: HttpRequest):
    name = req.params.get('name')
    if name is None:
        raise ValidationError("Request worked, but you didn't give me a name!")
    if len(req.params) > 1:
        raise ValidationError("You gave me too many parameters!")
    
    return {"name": name}


# -----------------------------------------------------------------------------
# For local calls

if __name__ == "__main__":
    # Run a test and output the result
    test_request = HttpRequest('GET', 'url', params={"name": "Test"}, body=bytes())
    r = main(test_request)  # type: ignore
    print(r.status_code, ":", r.get_body().decode("utf-8"))