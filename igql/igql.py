import json

from anyapi import AnyAPI
from anyapi.proxy_handlers import RateLimitProxy
from requests.exceptions import ChunkedEncodingError

from . import constants
from .exceptions import MaxRetries, NotFound, RateLimitExceed
from .hashtag import Hashtag
from .location import Location
from .media import Media
from .user import User
from .utils import get_shared_data, get_value_deep_key, set_instagram_gis


class InstagramGraphQL:
    loads = json.loads
    dumps = json.dumps

    def __init__(self, rhx_gis="", sessionid="", proxies=[], max_retries=3):
        self.last_response = {}
        self.max_retries = max_retries

        self.api = AnyAPI(
            constants.BASE_URL,
            default_headers={
                "user-agent": constants.USER_AGENT,
                "cookie": f"sessionid={sessionid}",
            },
            scoped_call=self.__retry,
            **(
                {
                    "proxy_configuration": {
                        "default": None,
                        "proxies": proxies,
                        "paths": {"/query": 100},
                    },
                    "proxy_handler": RateLimitProxy,
                }
                if proxies
                else {}
            ),
        )

        self.api._filter_response = [
            InstagramGraphQL.__rate_limit_exceed,
            InstagramGraphQL.__user_not_found,
            InstagramGraphQL.__hashtag_not_found,
            InstagramGraphQL.__location_not_found,
            InstagramGraphQL.__set_as_json,
            InstagramGraphQL.__media_not_found,
            self.__set_last_response,
        ]

        if not rhx_gis:
            rhx_gis = get_shared_data(self.api)["rhx_gis"]
        self.api._filter_request.append(
            lambda kwargs: set_instagram_gis(kwargs, rhx_gis)
        )

    def __retry(self, request, retries=0):
        try:
            return request()
        except ChunkedEncodingError as e:
            if retries != self.max_retries:
                return self.__retry(request, retries=retries + 1)
            else:
                raise e

    @staticmethod
    def __set_as_json(kwargs, response):
        if kwargs["path"] == "/query":
            return InstagramGraphQL.loads(response.text)
        return response.text

    def __set_last_response(self, _, response):
        self.last_response = response
        return response

    @staticmethod
    def __rate_limit_exceed(_, response):
        if response.status_code == 429:
            raise RateLimitExceed("Rate limit exceed!")

        return response

    @staticmethod
    def __media_not_found(kwargs, response):
        if kwargs["params"].get("query_hash") == constants.GET_MEDIA[
            "hash"
        ] and not response["data"].get("shortcode_media"):
            raise NotFound("Media not found!")

        return response

    @staticmethod
    def __user_not_found(kwargs, response):
        if (
            response.status_code == 404
            and kwargs["path"].split("/")[1] not in constants.FORBIDDEN_USERNAMES
        ):
            raise NotFound("User not found!")

        return response

    @staticmethod
    def __hashtag_not_found(kwargs, response):
        if response.status_code == 404 and kwargs["path"].startswith("/explore/tags/"):
            raise NotFound("Hashtag not found!")

        return response

    @staticmethod
    def __location_not_found(kwargs, response):
        if response.status_code == 404 and kwargs["path"].startswith(
            "/explore/locations/"
        ):
            raise NotFound("Location not found!")

        return response

    def get_media(self, shortcode, variables={}):
        response = self.api.query.GET(
            params={
                "query_hash": constants.GET_MEDIA["hash"],
                "variables": InstagramGraphQL.dumps(
                    {
                        **constants.GET_MEDIA["variables"],
                        "shortcode": shortcode,
                        **variables,
                    }
                ),
            }
        )

        return Media(response, self.api)

    def get_user(self, username):
        response = get_value_deep_key(
            get_shared_data(self.api, path=username), constants.GET_USER["keys"][1]
        )

        return User({"data": {"user": response}}, self.api)

    def get_hashtag(self, name):
        response = get_value_deep_key(
            get_shared_data(self.api, path=f"explore/tags/{name}/"),
            constants.GET_HASHTAG["keys"][1],
        )

        return Hashtag({"data": {"hashtag": response}}, self.api)

    def get_location(self, location_id):
        response = get_value_deep_key(
            get_shared_data(self.api, path=f"explore/locations/{location_id}/"),
            constants.GET_LOCATION["keys"][1],
        )

        return Location({"data": {"location": response}}, self.api)
