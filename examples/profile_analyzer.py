from igql import InstagramGraphQL
from collections import Counter


def get_tags(caption):
    if not caption or caption == "No photo description available.":
        return None
    return [tag.strip() for tag in caption.split(':')[1].replace(' and ', ',').split(',')]
    # Example accessibility_caption: "Image may contain: sky, cloud and outdoor"


igql_api = InstagramGraphQL()
user = igql_api.get_user(username, fetch_data=True)

tag_counter = Counter()
for media in user.timeline:
    tag_counter.update(get_tags(media.data.get('accessibility_caption')))


for media_batch in user.iterate_more_timeline_media(fetch_data=True):
    for media in media_batch:
        tag_counter.update(get_tags(media.data.get('accessibility_caption')))

print(tag_counter)
