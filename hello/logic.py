from wrappers import http
from errors import ValidationError

from azure.functions import HttpRequest


@http(template="hello/template.html")
def main(**inputs: dict):
    name = validate(inputs)
    return {"name": name}


def validate(inputs: dict):
    if inputs.get("name"):
        return inputs.get("name")
    
    raise ValidationError("Request worked, but you didn't give me a name!")


# -----------------------------------------------------------------------------
# For local calls

if __name__ == "__main__":
    # Run a test and output the result
    test_request = HttpRequest(
        'POST',
        'not-used.url',
        params={"name": "Test"},
        body=bytes()
    )
    response = main(test_request)
    print(
        response.status_code, ":",
        response.get_body().decode("utf-8")
    )