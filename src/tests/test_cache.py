from __future__ import absolute_import, unicode_literals

import os
import shutil

from imdbpie import Imdb


def setup_function(function):
    shutil.rmtree(Imdb().cache_dir, ignore_errors=True)


def _get_cache_size(cache_dir):
    """ Returns a count of the items in the cache """
    cache = os.path.exists(cache_dir)
    if not cache:
        return 0
    _, _, cache_files = next(os.walk(cache_dir))
    return len(cache_files)


def test_cache_populated():
    """ Tests the cache is populated correctly """
    imdb = Imdb(cache=True)

    assert _get_cache_size(imdb.cache_dir) == 0
    movie = imdb.get_title_by_id("tt0382932")
    # Make a 2nd call to ensure no duplicate cache items created
    imdb.get_title_by_id("tt0382932")

    # find makes 3 api calls
    assert _get_cache_size(imdb.cache_dir) == 3
    assert movie.title == 'Ratatouille'


def test_cache_not_populated_when_disabled():
    """ Tests the cache is not populated when disabled (default) """
    imdb = Imdb()
    assert _get_cache_size(imdb.cache_dir) == 0
    imdb.get_title_by_id("tt0382932")
    assert _get_cache_size(imdb.cache_dir) == 0
