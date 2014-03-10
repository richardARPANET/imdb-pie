from imdbpie import Imdb
import unittest
import re

imdb = Imdb({'anonymize': False})
movie = imdb.find_movie_by_id("tt0382932")


class TestTitle(unittest.TestCase):

    @staticmethod
    def valid_poster(poster_url):
        match = re.findall(r'http://ia.media-imdb.com/images/.*/', poster_url)[0]
        if match:
            return True
        else:
            return False

    def test_title(self):
        self.assertEqual(movie.title, 'Ratatouille')

    def test_imdb_id(self):
        self.assertEqual(movie.imdb_id, 'tt0382932')

    def test_tagline(self):
        self.assertEqual(movie.tagline, 'Dinner is served... Summer 2007')

    def test_plot(self):
        self.assertIsNotNone(movie.plot)

    def test_runtime(self):
        self.assertIsNotNone(movie.runtime)

    def test_rating(self):
        self.assertTrue(str(movie.rating).isdigit())

    def test_poster_url(self):
        self.assertTrue(self.valid_poster(movie.poster_url))

    def test_release_date(self):
        self.assertIsNotNone(movie.release_date)

    def test_certification(self):
        self.assertIsNotNone(movie.certification)

    def test_trailers(self):
        self.assertIsNotNone(movie.trailers)

    def test_genres(self):
        self.assertIsNotNone(movie.genres)

    def test_directors(self):
        self.assertIsNotNone(movie.directors_summary)

    def test_writers(self):
        self.assertIsNotNone(movie.writers_summary)

if __name__ == '__main__':
    unittest.main()
