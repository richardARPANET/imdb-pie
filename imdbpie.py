import json
import time
import requests
import urllib.parse
import hashlib
import re
import itertools

base_uri = 'app.imdb.com'
api_key = '2wex6aeu6a8q9e49k7sfvufd6rhh0n'
sha1_key = hashlib.sha1(api_key.encode('utf-8')).hexdigest()

class Imdb:

    def __init__( self, options=None ):
        if options is None:
            options = {}
            
        self.options = options

        if options.get('anonymize') is True:
            global base_uri
            base_uri = 'youtubeproxy.org/default.aspx?prx=https://{0}'.format(base_uri)


    def build_url(self, path, params):
        default_params = {"api" : "v1", "appid" : "iphone1_1", "apiPolicy" : "app1_1", "apiKey" : sha1_key, "locale" : "en_US", "timestamp" : int(time.time())}

        query_params = dict(itertools.chain(default_params.items(),
                                            params.items()))
        query_params = urllib.parse.urlencode(query_params)
        return 'https://{0}{1}?{2}'.format(base_uri, path, query_params)


    def find_movie_by_id(self, imdb_id):
        url = self.build_url('/title/maindetails', {'tconst' : imdb_id})
        result = self.get(url)
        movie = Movie(result["data"])
        return movie


    def filter_out(self, string):
        return string not in ('id', 'title')


    def find_by_title(self, title):
        default_find_by_title_params = {"json" : "1", "nr" : 1, "tt": "on", "q" : title}
        query_params = urllib.parse.urlencode(default_find_by_title_params)
        results = self.get('http://www.imdb.com/xml/find?{0}'.format(query_params))

        keys = ["title_popular", "title_exact", "title_approx", "title_substring"]
        data = results
        movie_results = {}

        for i, key in enumerate(keys):
            if key in data:
                for j,r in enumerate(filter(self.filter_out, data[key])):
                    year_match = re.findall(r'(\d{4})', r['title_description'])
                    year = year_match[0] if len(year_match) > 0 else None

                    movie_results[i+j] = {'title' : r["title"], 'year' : year, 'imdb_id' : r["id"]}
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
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B5097d Safari/6531.22.7'})
        return json.loads(r.text)


class Person:
    def __init__( self, options=None):
        if options is None:
            options = {}

        self.name = options["name"]["name"]
        self.imdb_id = options["name"]["nconst"]
        self.role = options["char"] if "char" in options else None

class Movie:
    def __init__( self, options=None):
        if options is None:
            options = {}

        #parse info
        self.imdb_id = options["tconst"]
        self.title = options["title"]
        self.tagline = options["tagline"] if "tagline" in options else None
        self.plot = options["plot"]["outline"] if "plot" in options else None
        self.runtime = str(round((options["runtime"]["time"]/60))) + ' min' if "runtime" in options else None
        self.rating = options["rating"] if "rating" in options else None
        self.poster_url = options["image"]["url"] if "image" in options else None
        self.release_date = options["release_date"]["normal"] if "release_date" in options and options["release_date"]["normal"] else None
        self.certification = options["certificate"]["certificate"] if options["certificate"] and options["certificate"]["certificate"] else None
        self.genres = options["genres"] or []
        self.trailer_url = options["trailer"]["slates"][0]["url"] if("trailer" in options and options["trailer"]["slates"] and options["trailer"]["slates"][0]) else None

        #parse directors
        self.directors = {}
        if options["directors_summary"]:
            for key, value in enumerate(options["directors_summary"]):
                self.directors[key] = Person(value)

        #parse actors
        self.actors = {}
        if options["cast_summary"]:
            for key, value in enumerate(options["cast_summary"]):
                self.actors[key] = Person(value)

        #parse writers
        self.writers = {}
        if options["cast_summary"]:
            for key, value in enumerate(options["writers_summary"]):
                self.writers[key] = Person(value)

        #parse trailers
        self.trailers = {}
        if "trailer" in options and options["trailer"]["encodings"]:
            for k, v in options["trailer"]["encodings"].items():
                self.trailers[v["format"]] = v["url"]

