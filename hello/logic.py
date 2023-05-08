from typing import Optional
from wrappers import http
from errors import ValidationError

from azure.functions import HttpRequest


@http(template="hello/template.html")
def main(name: Optional[str] = None, **kwargs):
    
    if name is None:
        raise ValidationError("Request worked, but you didn't give me a name!")
    if len(kwargs) > 0:
        raise ValidationError(f"I don't know what {list(kwargs.keys())} are!")
    
    return {"name": name}


# -----------------------------------------------------------------------------
# For local calls

if __name__ == "__main__":
    # Run a test and output the result
    test_request = HttpRequest('GET', 'url', params={"name": "Test"}, body=bytes())
    r = main(test_request)
    print(r.status_code, ":", r.get_body().decode("utf-8"))