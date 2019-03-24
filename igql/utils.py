from hashlib import md5

import igql

from .constants import IG_URL


def set_instagram_gis(kwargs, rhx_gis):
    if "variables" in kwargs["params"]:
        kwargs["headers"]["x-instagram-gis"] = md5(
            (f'{rhx_gis}:{kwargs["params"]["variables"]}').encode()
        ).hexdigest()
    return kwargs


def get_shared_data(api, path="instagram"):
    response = api.GET(url=f"{IG_URL}/{path}")
    response = response.split("window._sharedData = ")[1]
    response = response.split(";</script>")[0]
    response = igql.InstagramGraphQL.loads(response)

    return response


def paginator(api, data, keys, params):
    yield data[keys[0]]["edges"]

    has_next_page = data[keys[0]]["page_info"]["has_next_page"]
    end_cursor = data[keys[0]]["page_info"]["end_cursor"]

    while has_next_page:
        if isinstance(params["variables"], str):
            params["variables"] = igql.InstagramGraphQL.loads(params["variables"])
        params["variables"]["after"] = end_cursor
        params["variables"] = igql.InstagramGraphQL.dumps(params["variables"])

        data = get_value_deep_key(api.query.GET(params=params), keys[1])

        has_next_page = data[keys[0]]["page_info"]["has_next_page"]
        end_cursor = data[keys[0]]["page_info"]["end_cursor"]

        yield data[keys[0]]["edges"]


def get_value_deep_key(data, keys):
    for key in keys:
        data = data[key]
    return data
