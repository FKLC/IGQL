import json

from .media import Media


class Hashtag:
    def __init__(self, data, igql, fetch_comments=False):
        self.igql = igql
        self.data = data
        self.last_response = data

        self.name = data['name']
        self.hashtag_id = data['id']
        self.profile_pic = data['profile_pic_url']
        self.top_posts = [
            Media(media_data['node'], self.igql, fetch_comments=fetch_comments)
            for media_data in data['edge_hashtag_to_top_posts']['edges']
        ]
        self.recent_media = [
            Media(
                media_data['node'], self.igql, fetch_comments=fetch_comments)
            for media_data in data['edge_hashtag_to_media']['edges']
        ]

        self._recent_media_has_next_page = data['edge_hashtag_to_media'][
            'page_info']['has_next_page']
        self._recent_media_cursor = data['edge_hashtag_to_media']['page_info'][
            'end_cursor']

    def iterate_more_recent_media(self, reset=False, fetch_comments=False):
        if reset:
            self._recent_media_has_next_page = data['edge_hashtag_to_media'][
                'page_info']['has_next_page']
            self._recent_media_cursor = data['edge_hashtag_to_media'][
                'page_info']['end_cursor']
        while self._recent_media_has_next_page:
            params = {
                'query_hash':
                self.igql._QUERY_HASHES['load_more_hashtag_recent_media'],
                'variables': json.dumps({
                    'tag_name': self.name,
                    'first': 12,
                    'after': self._recent_media_cursor,
                },
                separators=(',', ':'))
            }

            self.last_response = self.igql.gql_api.query.GET(
                params=params).json()['data']['hashtag']

            self._recent_media_has_next_page = self.last_response[
                'edge_hashtag_to_media']['page_info']['has_next_page']
            self._recent_media_cursor = self.last_response[
                'edge_hashtag_to_media']['page_info']['end_cursor']

            yield [
                Media(
                    media_data['node'],
                    self.igql,
                    fetch_comments=fetch_comments) for media_data in self.
                last_response['edge_hashtag_to_media']['edges']
            ]
