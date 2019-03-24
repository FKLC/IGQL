import igql

from . import constants
from .utils import get_value_deep_key, paginator


class Hashtag:
    def __init__(self, data, api):
        self.api = api
        self.data = data

    def recent_media(self, variables={}):
        data = get_value_deep_key(self.data, constants.LOAD_HASHTAG["keys"][1])
        return paginator(
            self.api,
            data,
            constants.LOAD_HASHTAG["keys"],
            {
                "query_hash": constants.LOAD_HASHTAG["hash"],
                "variables": {
                    **constants.LOAD_HASHTAG["variables"],
                    "tag_name": data["name"],
                    **variables,
                },
            },
        )

    @property
    def top_posts(self):
        # Since there is no pagination leave it hardcoded.
        return get_value_deep_key(self.data, constants.LOAD_HASHTAG["keys"][1])[
            "edge_hashtag_to_top_posts"
        ]["edges"]
