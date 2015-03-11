from __future__ import absolute_import, unicode_literals

import os
import re
import json
import time
import random
import hashlib
import logging
import datetime

import requests
from six.moves import html_parser
from six.moves.urllib.parse import urlencode

from imdbpie.objects import Image, Title, Person, Review
from imdbpie.constants import BASE_URI, SHA1_KEY, USER_AGENTS

logger = logging.getLogger(__name__)


class Imdb(object):

    def __init__(self, locale=None, anonymize=None, exclude_episodes=None,
                 user_agent=None, cache=None, cache_dir=None):
        self.timestamp = time.mktime(datetime.date.today().timetuple())
        self.user_agent = user_agent or random.choice(USER_AGENTS)
        self.locale = locale or 'en_US'
        base_uri_proxy = (
            'aniscartujo.com/webproxy/default.aspx?prx=https://{0}'.format(
                BASE_URI)
        )
        self.base_uri = base_uri_proxy if anonymize is True else BASE_URI
        self.exclude_episodes = True if exclude_episodes is True else False
        self.caching_enabled = True if cache is True else False
        self.cache_dir = cache_dir or '/tmp/imdbpiecache'

    def build_url(self, path, params):
        default_params = {
            "api": "v1",
            "appid": "iphone1_1",
            "apiPolicy": "app1_1",
            "apiKey": SHA1_KEY,
            "locale": self.locale,
            "timestamp": self.timestamp
        }

        query_params = dict(
            list(default_params.items()) + list(params.items())
        )
        query_params = urlencode(query_params)
        url = 'https://{0}{1}?{2}'.format(self.base_uri, path, query_params)
        return url

    def find_movie_by_id(self, imdb_id):
        url = self.build_url('/title/maindetails', {'tconst': imdb_id})
        response = self.get(url)
        if response is None:
            return None

        # if the response is a re-dir, see imdb id tt0000021 for e.g...
        if (
            response["data"].get('tconst') !=
            response["data"].get('news', {}).get('channel')
        ):
            return None

        # get the full cast information, add key if not present
        response["data"][str("credits")] = self._get_credits(imdb_id)
        response['data']['plots'] = self.get_plots(imdb_id)

        if (
            self.exclude_episodes is True and
            response["data"].get('type') == 'tv_episode'
        ):
            return None
        title = Title(data=response["data"])
        return title

    def get_plots(self, imdb_id):
        url = self.build_url('/title/plot', {'tconst': imdb_id})
        response = self.get(url)

        if response['data']['tconst'] != imdb_id:  # pragma: no cover
            return []

        plots = response['data'].get('plots', [])
        return [plot.get('text') for plot in plots]

    def _get_credits(self, imdb_id):
        url = self.build_url('/title/fullcredits', {'tconst': imdb_id})
        response = self.get(url)

        if response is None:
            return None

        return response.get('data').get('credits')

    def _get_reviews(self, imdb_id):
        url = self.build_url('/title/usercomments', {'tconst': imdb_id})
        response = self.get(url)

        if response is None:
            return None

        return response.get('data').get('user_comments')

    def title_exists(self, imdb_id):
        titles = self.find_movie_by_id(imdb_id)
        return True if titles else False

    def find_by_title(self, title):
        default_find_by_title_params = {
            'json': '1',
            'nr': 1,
            'tt': 'on',
            'q': title
        }
        query_params = urlencode(default_find_by_title_params)
        results = self.get(
            ('http://www.imdb.com/xml/find?{0}').format(query_params)
        )

        keys = (
            'title_popular',
            'title_exact',
            'title_approx',
            'title_substring'
        )
        title_results = []

        html_unescaped = html_parser.HTMLParser().unescape

        # Loop through all results and build a list with popular matches first
        for key in keys:
            if key in results:
                for r in results[key]:
                    year_match = re.search(r'(\d{4})', r['title_description'])
                    year = year_match.group(0) if year_match else None

                    title_match = {
                        'title': html_unescaped(r['title']),
                        'year': year,
                        'imdb_id': r['id']
                    }
                    title_results.append(title_match)

        return title_results

    def top_250(self):
        url = self.build_url('/chart/top', {})
        response = self.get(url)
        return response["data"]["list"]["list"]

    def popular_shows(self):
        url = self.build_url('/chart/tv', {})
        response = self.get(url)
        return response["data"]["list"]

    def _get_images(self, response):
        images = []

        for image_data in response.get('data').get('photos', []):
            images.append(Image(image_data))

        return images

    def title_images(self, imdb_id):
        url = self.build_url('/title/photos', {'tconst': imdb_id})
        response = self.get(url)
        return self._get_images(response)

    def title_reviews(self, imdb_id):
        """
        Retrieves reviews for a title ordered by 'Best' descending
        """
        user_comments = self._get_reviews(imdb_id)

        if not user_comments:
            return None

        title_reviews = []

        for review_data in user_comments:
            title_reviews.append(Review(review_data))
        return title_reviews

    def person_images(self, imdb_id):
        url = self.build_url('/name/photos', {'nconst': imdb_id})
        response = self.get(url)
        return self._get_images(response)

    def _get_cache_item_path(self, url):
        """
        Generates a cache location for a given api call.
        Returns a file path
        """
        cache_dir = self.cache_dir
        m = hashlib.md5()
        m.update(url.encode('utf-8'))
        cache_key = m.hexdigest()

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        return os.path.join(cache_dir, cache_key + '.cache')

    def _get_cached_response(self, file_path):
        """ Retrieves response from cache """
        if os.path.exists(file_path):
            logger.info('retrieving from cache: %s', file_path)

            with open(file_path, 'r+') as resp_data:
                cached_resp = json.load(resp_data)

            if cached_resp.get('exp') > self.timestamp:
                return cached_resp
            else:  # pragma: no cover
                logger.info('cached expired, removing: %s', file_path)
                os.remove(file_path)
        return None

    @staticmethod
    def _cache_response(file_path, resp):
        with open(file_path, 'w+') as f:
            json.dump(resp, f)

    def get(self, url):
        if self.caching_enabled:
            cached_item_path = self._get_cache_item_path(url)
            cached_resp = self._get_cached_response(cached_item_path)
            if cached_resp:
                return cached_resp

        r = requests.get(url, headers={'User-Agent': self.user_agent})
        response = json.loads(r.content.decode('utf-8'))

        if self.caching_enabled:
            self._cache_response(cached_item_path, response)

        if response.get('error'):
            return None

        return response
