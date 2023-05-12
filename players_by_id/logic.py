import json

from azure.functions import HttpRequest

from wrappers import http


players_by_id = {
    "95024a36": {"name": "Alec"},
    "83ea724e": {"name": "Tay"}
}

@http()
def main(req: HttpRequest):
    player_id = req.route_params["player_id"]
    return json.dumps(players_by_id[player_id])


# -----------------------------------------------------------------------------
# For local calls

if __name__ == "__main__":
    # Run a test and output the result
    test_request = HttpRequest('GET', 'url', body=bytes())
    r = main(test_request)  # type: ignore
    print(r.status_code, ":", r.get_body().decode("utf-8"))