from imdbpie import Imdb
import unittest

imdb = Imdb({'anonymize': False})


class TestSearch(unittest.TestCase):

    def test_batman(self):
        self.results = imdb.find_by_title("batman")
        self.assertGreater(len(self.results), 15)

    def test_truman(self):
        self.results = imdb.find_by_title("the truman show")
        self.assertGreater(len(self.results), 1)

    def test_bad_search(self):
        self.results = imdb.find_by_title("fdlfj494llsidjg49hkdg")
        self.assertEquals(len(self.results), 0)

    def test_top_250(self):
        self.movies = imdb.top_250()
        self.assertTrue(isinstance(self.movies[0], dict))

    def test_popular_shows(self):
        self.shows = imdb.popular_shows()
        self.assertTrue(isinstance(self.shows[0], dict))


if __name__ == '__main__':
    unittest.main()
