import json


class Media:
    def __init__(self, data, igql, fetch_comments=False):
        self.igql = igql
        self.data = data
        self.last_response = data

        self.shortcode = data['shortcode']
        self.display_url = data['display_url']
        self.like_count = data['edge_media_preview_like']['count']
        try:
            self.comments = data['edge_media_to_comment']['edges']

            self._comments_has_next_page = data['edge_media_to_comment'][
                'page_info']['has_next_page']
            self._comments_end_cursor = data['edge_media_to_comment'][
                'page_info']['end_cursor']
        except:
            if fetch_comments:
                self._fetch_comments()
            else:
                self.comments = None

                self._comments_has_next_page = False
                self._comments_end_cursor = None
        self._liked_by_has_next_page = True
        self._liked_by_end_cursor = None

    def _fetch_comments(self):
        media = self.igql.get_media(self.shortcode)
        self.comments = media.comments
        self.data['edge_media_to_comment']['page_info'] = {
            'has_next_page': media._comments_has_next_page,
            'end_cursor': media._comments_end_cursor
        }
        self._comments_has_next_page = media._comments_has_next_page
        self._comments_end_cursor = media._comments_end_cursor

        return media.comments

    def iterate_more_comments(self, reset=False):
        if not self.comments:
            yield self._fetch_comments()
        if reset:
            self._comments_has_next_page = self.data[
                'edge_media_to_comment']['page_info']['has_next_page']
            self._comments_end_cursor = self.data['edge_media_to_comment'][
                'page_info']['end_cursor']
        while self._comments_has_next_page:
            params = {
                'query_hash':
                self.igql._QUERY_HASHES['load_more_comments'],
                'variables': json.dumps({
                    'shortcode': self.shortcode,
                    'first': 40,
                    'after': self._comments_end_cursor
                },
                separators=(',', ':'))
            }

            self.last_response = self.igql.gql_api.query___get(
                params=params).json()['data']['shortcode_media']

            self._comments_has_next_page = self.last_response[
                'edge_media_to_comment']['page_info']['has_next_page']
            self._comments_end_cursor = self.last_response[
                'edge_media_to_comment']['page_info']['end_cursor']

            yield self.last_response['edge_media_to_comment']['edges']

    def iterate_liked_by(self, reset=False):
        if reset:
            self._liked_by_has_next_page = True
            self._liked_by_end_cursor = None
        while self._liked_by_has_next_page:
            params = {
                'query_hash':
                self.igql._QUERY_HASHES['load_liked_by'],
                'variables': json.dumps({
                    'shortcode': self.shortcode,
                    'include_reel': True,
                    'first': 24,
                },
                separators=(',', ':')),
            }
            if self._liked_by_end_cursor:
                params['after'] = self._liked_by_end_cursor

            self.last_response = self.igql.gql_api.query___get(
                params=params).json()['data']['shortcode_media']

            self._liked_by_has_next_page = self.last_response['edge_liked_by'][
                'page_info']['has_next_page']
            self._liked_by_end_cursor = self.last_response['edge_liked_by'][
                'page_info']['end_cursor']

            yield self.last_response['edge_liked_by']['edges']
