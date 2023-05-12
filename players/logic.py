import logging
from azure.functions import HttpRequest

from wrappers import http
from errors import ValidationError


players = [
    {"id": "95024a36", "name": "Alec"},
    {"id": "83ea724e", "name": "Tay"}
]

@http()
def main(req: HttpRequest):
    logging.info(req)
    logging.info(req.url)
    logging.info(req.params)
    
    return [
        {"id": "95024a36", "name": "Alec"},
        {"id": "83ea724e", "name": "Tay"}
    ]


# -----------------------------------------------------------------------------
# For local calls

if __name__ == "__main__":
    # Run a test and output the result
    test_request = HttpRequest('GET', 'url', body=bytes())
    r = main(test_request)  # type: ignore
    print(r.status_code, ":", r.get_body().decode("utf-8"))