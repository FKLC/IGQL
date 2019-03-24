# End of support
According to this issue [#1]https://github.com/FKLC/IGQL/issues/1) [Instaloader](https://github.com/instaloader/instaloader) is already doing what this library does so why reinvent the wheel while it exists also I'm so sorry about wasting your time using this library instead of Instaloader it is much better than IGQL. @ogencoglu actually created issue about it but I think when I checked the source of [Instaloader](https://github.com/instaloader/instaloader) I accidentally typed something else instead of `graphql`. Also as you can guess I'm not going to document new API change but I'll upload new version to PyPI so if still want to use this library you should run `pip install igql==1.1.0` to use old documented version.

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
* There is a lot of cool data returned by GraphQL. For example `accessibility_caption` which you can train your image classifier through it

###### NOTE: This is basically a API to collet data not for uploading or interacting with media. If you want more advanced IG library you should check [LevPasha's Instagram-API-python](https://github.com/LevPasha/Instagram-API-python) package.

### Getting all media of a user
```python
from igql import InstagramGraphQL


igql_api = InstagramGraphQL()

user = igql_api.get_user('instagram')
for media in user.timeline():
    print(media)
```

## Installation
Library is avaible on PyPi so just run

```
pip install igql==1.1.0
```


# To learn more check [wiki page](https://github.com/FKLC/IGQL/wiki).
