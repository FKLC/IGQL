from hashlib import md5
from anyapi import AnyAPI
import json

from .media import Media
from .user import User
from .hashtag import Hashtag
from .location import Location
from .exceptions import RateLimitExceed, NotFound


class InstagramGraphQL:
    _IG_URL = 'https://www.instagram.com'
    _BASE_URL = f'{_IG_URL}/graphql/'
    _QUERY_HASHES = {
        'get_media': '49699cdb479dd5664863d4b647ada1f7',
        'load_more_comments': 'f0986789a5c5d17c2400faebf16efd0d',
        'load_liked_by': 'e0f59e4a1c8d78d0161873bc2ee7ec44',
        'load_more_timeline_media': 'e6a78c2942f1370ea50e04c9a45ebc44',
        'load_more_hashtag_recent_media': 'f92f56d47dc7a55b606908374b43a314',
        'load_more_location_recent_media': '1b84447a4d8b6d6d0426fefb34514485',
    }
    _USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    _FORBIDDEN_USERNAMES = ['graphql', 'explore']

    def __init__(self, rhx_gis='', sessionid='', proxies=[]):
        self.last_response = {}
        proxy_configration = {
            'default': None,
            'proxies': proxies,
            'paths': {
                '/query': 100
            }
        }
        self.gql_api = AnyAPI(
            self._BASE_URL,
            default_headers={
                'user-agent': self._USER_AGENT,
                'cookie': f'sessionid={sessionid}',
            },
            proxy_configration=proxy_configration)
        if not rhx_gis:
            rhx_gis = self._get_shared_data()['rhx_gis']
        self.rhx_gis = rhx_gis

        self.gql_api._filter_headers.append(self._set_instagram_gis)
        self.gql_api._filter_response.append(self._raise_rate_limit_exceed)
        self.gql_api._filter_response.append(self._raise_media_not_found)
        self.gql_api._filter_response.append(self._raise_user_not_found)
        self.gql_api._filter_response.append(self._raise_hashtag_not_found)
        self.gql_api._filter_response.append(self._raise_location_not_found)

    def get_media(self, shortcode):
        params = {
            'query_hash': self._QUERY_HASHES['get_media'],
            'variables': json.dumps({
                'shortcode': shortcode,
                'child_comment_count': 0,
                'fetch_comment_count': 40,
                'parent_comment_count': 0,
                'has_threaded_comments': False
            },
            separators=(',', ':'))
        }

        self.last_response = self.gql_api.query.GET(
            params=params).json()['data']['shortcode_media']

        return Media(self.last_response, self)

    def get_user(self, username, fetch_comments=False):
        self.last_response = self._get_shared_data(
            username)['entry_data']['ProfilePage'][0]['graphql']['user']

        return User(self.last_response, self, fetch_comments=fetch_comments)

    def get_hashtag(self, name, fetch_comments=False):
        self.last_response = self._get_shared_data(f'explore/tags/{name}/')[
            'entry_data']['TagPage'][0]['graphql']['hashtag']

        return Hashtag(self.last_response, self)

    def get_location(self, location_id):
        self.last_response = self._get_shared_data(
            f'explore/locations/{location_id}/'
        )['entry_data']['LocationsPage'][0]['graphql']['location']

        return Location(self.last_response, self)

    def search(self, query):
        return self.gql_api.GET(
            url='https://www.instagram.com/web/search/topsearch/',
            params={
                'query': query
            }).json()

    def _get_shared_data(self, path='instagram'):
        self.last_response = self.gql_api.GET(url=f'{self._IG_URL}/{path}')
        self.last_response = self.last_response.text.split(
            'window._sharedData = ')[1]
        self.last_response = self.last_response.split(';</script>')[0]
        self.last_response = json.loads(self.last_response)

        return self.last_response

    def _set_instagram_gis(self, params, headers, **kwargs):
        if not params.get('variables'): return headers
        return {
            **headers, 'x-instagram-gis':
            md5((self.rhx_gis + ':' +
                 params['variables']).encode()).hexdigest()
        }

    def _raise_rate_limit_exceed(self, response, **kwargs):
        if response.status_code == 429 and response.json(
        )['message'] == 'rate limited':
            raise RateLimitExceed('Rate limit exceed!')

        return response

    def _raise_media_not_found(self, response, path, **kwargs):
        if response.status_code == 200 and path == 'query' and not response.json(
        )['data'].get(
                'shortcode_media', True):
            raise NotFound('Media not found!')

        return response

    def _raise_user_not_found(self, response, url, path, **kwargs):
        if response.status_code == 404 and path.split(
                    '/')[0] not in self._FORBIDDEN_USERNAMES:
            raise NotFound('User not found!')

        return response

    def _raise_hashtag_not_found(self, response, url, path, **kwargs):
        if response.status_code == 404 and url.startswith(
                f'{self._IG_URL}/explore/tags/'):
            raise NotFound('Hashtag not found!')

        return response

    def _raise_location_not_found(self, response, url, path, **kwargs):
        if response.status_code == 404 and url.startswith(
                f'{self._IG_URL}/explore/locations/'):
            raise NotFound('Location not found!')

        return response
