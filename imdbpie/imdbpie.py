import json
import time
import requests
from urllib import urlencode
import hashlib
import re
import HTMLParser

base_uri = 'app.imdb.com'
api_key = '2wex6aeu6a8q9e49k7sfvufd6rhh0n'
sha1_key = hashlib.sha1(api_key.encode('utf-8')).hexdigest()


class Imdb:

    def __init__(self, options=None):
        self.locale = 'en_US'
        self.base_uri = base_uri

        if options is None:
            options = {}
            
        self.options = options
        if options.get('anonymize') is True:
            self.base_uri = 'youtubeproxy.org/default.aspx?prx=https://{0}'.format(self.base_uri)

        if options.get('exclude_episodes') is True:
            self.exclude_episodes = True
        else:
            self.exclude_episodes = False

        if options.get('locale'):
            self.locale = options.get('locale')

    def build_url(self, path, params):
        default_params = {"api": "v1",
                          "appid": "iphone1_1",
                          "apiPolicy": "app1_1",
                          "apiKey": sha1_key,
                          "locale": self.locale,
                          "timestamp": int(time.time())}

        query_params = dict(default_params.items() + params.items())
        query_params = urlencode(query_params)
        return 'https://{0}{1}?{2}'.format(self.base_uri, path, query_params)

    def find_movie_by_id(self, imdb_id, json=False):
        imdb_id = self.validate_id(imdb_id)
        url = self.build_url('/title/maindetails', {'tconst': imdb_id})
        result = self.get(url)
        if 'error' in result:
            return False
        # if the result is a re-dir, see imdb id tt0000021 for e.g...
        if result["data"].get('tconst') != result["data"].get('news').get('channel'):
            return False

        #get the full cast information
        if 'credits' in result["data"]:
            result["data"]["credits"] = self.get_credits(imdb_id)

        if self.exclude_episodes is True and result["data"].get('type') == 'tv_episode':
            return False
        elif json is True:
            return result["data"]
        else:
            movie = Movie(**result["data"])
            return movie

    def get_credits(self, imdb_id):
        imdb_id = self.validate_id(imdb_id)
        url = self.build_url('/title/fullcredits', {'tconst': imdb_id})
        result = self.get(url)
        return result["data"]["credits"]

    def filter_out(self, string):
        return string not in ('id', 'title')

    def movie_exists(self, imdb_id):
        """
        Check with imdb, does a movie exist
        """
        imdb_id = self.validate_id(imdb_id)
        if imdb_id:
            results = self.find_movie_by_id(imdb_id)
            if results:
                return True
            else:
                return False
        else:
            return False

    def validate_id(self, imdb_id):
        """
        Check imdb id is a 7 digit number
        """
        match = re.findall(r'tt(\d+)', imdb_id, re.IGNORECASE)
        if match:
            id_num = match[0]
            if len(id_num) is not 7:
                #pad id to 7 digits
                id_num = id_num.zfill(7)
            return 'tt' + id_num
        else:
            return False

    def find_by_title(self, title):
        default_find_by_title_params = {'json': '1',
                                        'nr': 1,
                                        'tt': 'on',
                                        'q': title}
        query_params = urlencode(default_find_by_title_params)
        results = self.get(('http://www.imdb.com/'
                            'xml/find?{0}').format(query_params))

        keys = ['title_popular',
                'title_exact',
                'title_approx',
                'title_substring']
        movie_results = []

        html_unescape = HTMLParser.HTMLParser().unescape

        # Loop through all results and build a list with popular matches first
        for key in keys:
            if key in results:
                for r in results[key]:
                    year = None
                    year_match = re.search(r'(\d{4})', r['title_description'])
                    if year_match:
                        year = year_match.group(0)

                    movie_match = {
                        'title': html_unescape(r['title']),
                        'year': year,
                        'imdb_id': r['id']
                    }
                    movie_results.append(movie_match)

        return movie_results

    def top_250(self):
        url = self.build_url('/chart/top', {})
        result = self.get(url)
        return result["data"]["list"]["list"]

    def popular_shows(self):
        url = self.build_url('/chart/tv', {})
        result = self.get(url)
        return result["data"]["list"]

    def get(self, url):
        r = requests.get(url, headers={'User-Agent': '''Mozilla/5.0
        (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us)
        AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B5097d Safari/6531.22.7'''})
        return json.loads(r.text)


class Person(object):
    def __init__(self, **kwargs):
        p = kwargs['name']

        self.name = p.get('name')
        self.imdb_id = p.get('nconst')
        self.role = kwargs.get('char')
        self.job = kwargs.get('job')

    def __repr__(self):
        return '<Person: {0} ({1})>'.format(self.name.encode('utf-8'), self.imdb_id)


class Movie:
    def __init__(self, **kwargs):
        self.data = kwargs

        self.imdb_id = self.data.get('tconst')
        self.title = self.data.get('title')
        self.type = self.data.get('type')
        self.year = int(self.data.get('year'))
        self.tagline = self.data.get('tagline')
        self.plot = self.data.get('plot')
        self.runtime = self.data.get('runtime')
        self.rating = self.data.get('rating')
        self.genres = self.data.get('genres')
        self.votes = self.data.get('num_votes')

        self.plot_outline = None
        if 'plot' in self.data and 'outline' in self.data['plot']:
            self.plot_outline = self.data['plot']['outline']

        self.runtime = None
        if 'runtime' in self.data:
            #mins
            self.runtime = str(int((self.data['runtime']['time'] / 60)))

        self.poster_url = None
        if 'image' in self.data and 'url' in self.data['image']:
            self.poster_url = self.data['image']['url']

        self.cover_url = None
        if 'image' in self.data and 'url' in self.data['image']:
            self.cover_url = '{}_SX214_.jpg'.format(self.data['image']['url'].replace('.jpg', ''))

        self.release_date = None
        if 'release_date' in self.data and 'normal' in self.data['release_date']:
            self.release_date = self.data['release_date']['normal']

        self.certification = None
        if 'certificate' in self.data and 'certificate' in self.data['certificate']:
            self.certification = self.data['certificate']['certificate']

        self.trailer_img_url = None
        if ('trailer' in self.data and 'slates' in self.data['trailer'] and
                self.data['trailer']['slates']):
            self.trailer_img_url = self.data['trailer']['slates'][0]['url']

        # Directors
        self.directors = []
        if self.data.get('directors_summary'):
            for director in self.data['directors_summary']:
                self.directors.append(Person(**director))

        # Creators
        self.creators = []
        if self.data.get('creators'):
            for creator in self.data['creators']:
                self.creators.append(Person(**creator))

        # Cast summary
        self.cast_summary = []
        if self.data.get('cast_summary'):
            for cast in self.data['cast_summary']:
                self.cast_summary.append(Person(**cast))

        # Credits
        self.credits = []
        if self.data.get('credits'):
            for credit in self.data['credits']:
                """
                Possible tokens
                directors, cast, writers
                """
                if 'cast' in credit['token']:
                    for member in credit['list']:
                        self.credits.append(Person(**member))

        # Writers
        self.writers = []
        if self.data.get('writers_summary'):
            for writer in self.data['writers_summary']:
                self.writers.append(Person(**writer))

        # Trailers
        self.trailers = {}
        if 'trailer' in self.data and 'encodings' in self.data['trailer']:
            for k, v in self.data['trailer']['encodings'].items():
                self.trailers[v['format']] = v['url']