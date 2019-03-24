import igql

from . import constants
from .utils import get_value_deep_key, paginator


class Location:
    def __init__(self, data, api):
        self.api = api
        self.data = data

    def recent_media(self, variables={}):
        data = get_value_deep_key(self.data, constants.LOAD_LOCATION["keys"][1])
        return paginator(
            self.api,
            data,
            constants.LOAD_LOCATION["keys"],
            {
                "query_hash": constants.LOAD_LOCATION["hash"],
                "variables": {
                    **constants.LOAD_LOCATION["variables"],
                    "id": data["id"],
                    **variables,
                },
            },
        )

    @property
    def top_posts(self):
        # Since there is no pagination leave it hardcoded.
        return get_value_deep_key(self.data, constants.LOAD_LOCATION["keys"][1])[
            "edge_location_to_top_posts"
        ]["edges"]
