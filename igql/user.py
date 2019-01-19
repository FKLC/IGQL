import json

from .media import Media


class User:
    def __init__(self, data, igql, fetch_comments=False):
        self.igql = igql
        self.data = data
        self.last_response = data

        self.username = data['username']
        self.user_id = data['id']
        self.profile_pic = data['profile_pic_url_hd']
        self.follower_count = data['edge_followed_by']['count']
        self.following_count = data['edge_follow']['count']
        self.timeline = [
            Media(
                media_data['node'], self.igql, fetch_comments=fetch_comments)
            for media_data in data['edge_owner_to_timeline_media']['edges']
        ]

        self._timeline_has_next_page = data['edge_owner_to_timeline_media'][
            'page_info']['has_next_page']
        self._timeline_end_cursor = data['edge_owner_to_timeline_media'][
            'page_info']['end_cursor']

    def iterate_more_timeline_media(self, reset=False):
        if reset:
            self._timeline_has_next_page = data[
                'edge_owner_to_timeline_media']['page_info'][
                    'has_next_page']
            self._timeline_end_cursor = data[
                'edge_owner_to_timeline_media']['page_info']['end_cursor']
        while self._timeline_has_next_page:
            params = {
                'query_hash':
                self.igql._QUERY_HASHES['load_more_timeline_media'],
                'variables': json.dumps({
                    'id': self.user_id,
                    'first': 12,
                    'after': self._timeline_end_cursor,
                },
                separators=(',', ':'))
            }

            self.last_response = self.igql.gql_api.query___get(
                params=params).json()['data']['user']

            self._timeline_has_next_page = self.last_response[
                'edge_owner_to_timeline_media']['page_info'][
                    'has_next_page']
            self._timeline_end_cursor = self.last_response[
                'edge_owner_to_timeline_media']['page_info']['end_cursor']

            yield [
                Media(media_data['node'], self.igql) for media_data in
                self.last_response['edge_owner_to_timeline_media']['edges']
            ]
