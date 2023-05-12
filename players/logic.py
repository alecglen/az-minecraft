import json
import logging

from azure.functions import HttpRequest

from wrappers import http
from errors import ValidationError


players_by_id = {
    "95024a36": {"name": "Alec"},
    "83ea724e": {"name": "Tay"}
}

all_players = [
    {"id": "95024a36", "name": "Alec"},
    {"id": "83ea724e", "name": "Tay"}
]

@http()
def main(req: HttpRequest):
    logging.info(f"{req=}")
    logging.info(f"{req.url=}")
    logging.info(f"{req.params=}")
    logging.info(f"{req.route_params=}")
    
    if "player_id" in req.route_params:
        player_id = req.route_params["player_id"]
        if player_id not in players_by_id:
            raise ValidationError(f"Player with id {player_id} not found!")
        return json.dumps(players_by_id[player_id])
    
    return json.dumps(all_players)


# -----------------------------------------------------------------------------
# For local calls

if __name__ == "__main__":
    # Run a test and output the result
    test_request = HttpRequest('GET', 'url', body=bytes())
    r = main(test_request)  # type: ignore
    print(r.status_code, ":", r.get_body().decode("utf-8"))