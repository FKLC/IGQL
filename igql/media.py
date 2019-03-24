import igql

from . import constants
from .utils import get_value_deep_key, paginator


class Media:
    def __init__(self, data, api):
        self.api = api
        self.data = data

    def comments(self, variables={}):
        data = get_value_deep_key(self.data, constants.LOAD_COMMENTS["keys"][1])
        return paginator(
            self.api,
            data,
            constants.LOAD_COMMENTS["keys"],
            {
                "query_hash": constants.LOAD_COMMENTS["hash"],
                "variables": {
                    **constants.LOAD_COMMENTS["variables"],
                    "shortcode": data["shortcode"],
                    **variables,
                },
            },
        )

    def __first_liked_by(self, variables):
        return self.api.query.GET(
            params={
                "query_hash": constants.LOAD_LIKED_BY["hash"],
                "variables": igql.InstagramGraphQL.dumps(
                    {
                        **constants.LOAD_LIKED_BY["variables"],
                        "shortcode": get_value_deep_key(
                            self.data, constants.LOAD_LIKED_BY["keys"][1]
                        )["shortcode"],
                        **variables,
                    }
                ),
            }
        )

    def liked_by(self, variables={}):
        get_value_deep_key(self.data, constants.LOAD_LIKED_BY["keys"][1])[
            constants.LOAD_LIKED_BY["keys"][0]
        ] = get_value_deep_key(
            self.__first_liked_by(variables), constants.LOAD_LIKED_BY["keys"][1]
        )[
            constants.LOAD_LIKED_BY["keys"][0]
        ]

        data = get_value_deep_key(self.data, constants.LOAD_LIKED_BY["keys"][1])
        return paginator(
            self.api,
            data,
            constants.LOAD_LIKED_BY["keys"],
            {
                "query_hash": constants.LOAD_LIKED_BY["hash"],
                "variables": {
                    **constants.LOAD_LIKED_BY["variables"],
                    "shortcode": data["shortcode"],
                    **variables,
                },
            },
        )
