# InstagramGraphQL Unofficial API
Unofficial Instagram GraphQL API to collet data without authentication.

### Features
* Search for people, hashtags and locations
* Get media data
* Get hashtag data
* Get location data
* Get all comments
* Get all likes
* Get specific user posts
* With sessionid supplied you can get data from private accounts

###### NOTE: This is basically a API to collet data not for uploading or interacting with media. If you want more advanced IG library you should check [LevPasha's Instagram-API-python](https://github.com/LevPasha/Instagram-API-python) package.

### Getting all media of a user
```python
from igql import InstagramGraphQL


igql_api = InstagramGraphQL()

user = igql_api.get_user('instagram')
for media in user.timeline: # This is entry_data not the all media
    print(media.image_url)

for media_list in user.iterate_more_timeline_media():
    for media in media_list:
        print(media.image_url)
```

## Installation
Library is avaible on PyPi so just run

```
pip install igql
```


# To learn more check [wiki page](https://github.com/FKLC/IGQL/wiki).
