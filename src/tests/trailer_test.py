from __future__ import absolute_import, unicode_literals

from imdbpie import Imdb

imdb = Imdb({'anonymize': False})
movie = imdb.find_movie_by_id("tt0382932")


def test_trailer_url():
    movie.trailers is not None
