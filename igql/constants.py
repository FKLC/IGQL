# URLs
IG_URL = "https://www.instagram.com"
BASE_URL = f"{IG_URL}/graphql/"

# Queries
GET_MEDIA = {
    "hash": "477b65a610463740ccdb83135b2014db",
    "variables": {
        "shortcode": "",
        "child_comment_count": 3,
        "fetch_comment_count": 40,
        "parent_comment_count": 24,
        "has_threaded_comments": False,
    },
    "keys": ["", ["data", "shortcode_media"]],
}
LOAD_COMMENTS = {
    "hash": "f0986789a5c5d17c2400faebf16efd0d",
    "variables": {"shortcode": "", "first": 47, "after": ""},
    "keys": ["edge_media_to_comment", ["data", "shortcode_media"]],
}
LOAD_LIKED_BY = {
    "hash": "e0f59e4a1c8d78d0161873bc2ee7ec44",
    "variables": {"shortcode": "", "include_reel": True, "first": 24, "after": ""},
    "keys": ["edge_liked_by", ["data", "shortcode_media"]],
}
LOAD_TIMELINE = {
    "hash": "f2405b236d85e8296cf30347c9f08c2a",
    "variables": {"id": "", "first": 12, "after": ""},
    "keys": ["edge_owner_to_timeline_media", ["data", "user"]],
}
LOAD_HASHTAG = {
    "hash": "f92f56d47dc7a55b606908374b43a314",
    "variables": {"tag_name": "", "show_ranked": False, "first": 12, "after": ""},
    "keys": ["edge_hashtag_to_media", ["data", "hashtag"]],
}
LOAD_LOCATION = {
    "hash": "1b84447a4d8b6d6d0426fefb34514485",
    "variables": {"id": "", "first": 12, "after": ""},
    "keys": ["edge_location_to_media", ["data", "location"]],
}


# Direct Accesses
GET_USER = {"keys": ["", ["entry_data", "ProfilePage", 0, "graphql", "user"]]}
GET_HASHTAG = {"keys": ["", ["entry_data", "TagPage", 0, "graphql", "hashtag"]]}
GET_LOCATION = {"keys": ["", ["entry_data", "LocationsPage", 0, "graphql", "location"]]}

# Misc
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
FORBIDDEN_USERNAMES = ["graphql", "explore"]
