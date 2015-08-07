from __future__ import absolute_import, unicode_literals

import pytest
from imdbpie import Imdb
from imdbpie.imdbpie import requests_cache


@pytest.fixture(scope='function')
def set_up():
    requests_cache.CachedSession().cache.clear()
    assert _get_cache_size() == 0


def _get_cache_size():
    """ Returns a count of the items in the cache """
    return len(requests_cache.CachedSession().cache.responses.keys())


def test_cache_populated(set_up):
    """ Tests the cache is populated correctly """
    imdb = Imdb(cache=True)

    assert _get_cache_size() == 0
    title = imdb.get_title_by_id('tt0382932')
    # Make a 2nd call to ensure no duplicate cache items created
    title2 = imdb.get_title_by_id('tt0382932')
    # find makes 3 api calls
    assert _get_cache_size() == 3
    assert title.title == 'Ratatouille'
    assert title.data == title2.data


def test_cache_not_populated_when_disabled(set_up):
    """ Tests the cache is not populated when disabled (default) """
    imdb = Imdb()

    assert _get_cache_size() == 0
    imdb.get_title_by_id('tt0382932')
    assert _get_cache_size() == 0
