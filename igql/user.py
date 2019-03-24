import igql

from . import constants
from .utils import get_value_deep_key, paginator


class User:
    def __init__(self, data, api):
        self.api = api
        self.data = data

    def timeline(self, variables={}):
        data = get_value_deep_key(self.data, constants.LOAD_TIMELINE["keys"][1])
        return paginator(
            self.api,
            data,
            constants.LOAD_TIMELINE["keys"],
            {
                "query_hash": constants.LOAD_TIMELINE["hash"],
                "variables": {
                    **constants.LOAD_TIMELINE["variables"],
                    "id": data["id"],
                    **variables,
                },
            },
        )
