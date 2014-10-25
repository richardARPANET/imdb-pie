from __future__ import absolute_import
import os
import shutil
import unittest
from imdbpie import Imdb


class TestCache(unittest.TestCase):

    def setUp(self):
        self.imdb = Imdb()

    def tearDown(self):
        shutil.rmtree(self.imdb.cache_dir, ignore_errors=True)

    def _get_cache_size(self):
        """ Returns a count of the items in the cache """
        cache = os.path.exists(self.imdb.cache_dir)
        if not cache:
            return 0
        _, _, cache_files = os.walk(self.imdb.cache_dir).next()
        return len(cache_files)

    def test_cache_populated(self):
        """ Tests the cache is populated correctly """
        self.imdb = Imdb({'cache': True, 'cache_dir': '/tmp/imdbpie-test'})

        self.assertEqual(self._get_cache_size(), 0)
        movie = self.imdb.find_movie_by_id("tt0382932")
        # Make a 2nd call to ensure no duplicate cache items created
        self.imdb.find_movie_by_id("tt0382932")

        # find makes 2 api calls
        self.assertEqual(self._get_cache_size(), 2)
        self.assertEqual(movie.title, 'Ratatouille')

    def test_cache_not_populated_when_disabled(self):
        """ Tests the cache is not populated when disabled (default) """
        self.assertEqual(self._get_cache_size(), 0)
        self.imdb.find_movie_by_id("tt0382932")
        self.assertEqual(self._get_cache_size(), 0)


if __name__ == '__main__':
    unittest.main()
