from wrappers import http
from errors import ValidationError


@http(template="hello/template.html")
def main(**inputs: dict):
    name = validate(inputs)
    return {"name": name}


def validate(inputs: dict):
    if inputs.get("name"):
        return inputs.get("name")
    
    raise ValidationError("Request worked, but you didn't give me a name!")
