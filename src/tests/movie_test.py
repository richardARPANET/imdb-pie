from imdbpie import Imdb
try:
    import unittest2 as unittest  # for Python <= 2.6
except ImportError:
    import unittest
import re


class TestTitle(unittest.TestCase):

    def setUp(self):
        self.imdb = Imdb({'anonymize': False})
        self.movie = self.imdb.find_movie_by_id("tt0382932")

    @staticmethod
    def valid_poster(poster_url):
        match = re.findall(
            r'http://ia.media-imdb.com/images/.*/',
            poster_url
        )[0]
        return True if match else False

    def test_title(self):
        self.assertEqual(self.movie.title, 'Ratatouille')

    def test_imdb_id(self):
        self.assertEqual(self.movie.imdb_id, 'tt0382932')

    def test_tagline(self):
        self.assertEqual(self.movie.tagline, 'Dinner is served... Summer 2007')

    def test_plot(self):
        self.assertIsNotNone(self.movie.plots)

    def test_runtime(self):
        self.assertIsNotNone(self.movie.runtime)

    def test_rating(self):
        self.assertTrue(str(self.movie.rating).isdigit())

    def test_poster_url(self):
        self.assertTrue(self.valid_poster(self.movie.poster_url))

    def test_release_date(self):
        self.assertIsNotNone(self.movie.release_date)

    def test_certification(self):
        self.assertIsNotNone(self.movie.certification)

    def test_trailers(self):
        self.assertIsNotNone(self.movie.trailers)

    def test_genres(self):
        self.assertIsNotNone(self.movie.genres)

    def test_directors(self):
        self.assertIsNotNone(self.movie.directors_summary)

    def test_writers(self):
        self.assertIsNotNone(self.movie.writers_summary)

    def test_plot_and_plot_outline(self):
        title = self.imdb.find_movie_by_id('tt1588875')

        expected_plots = [(
            'A polar station on a desolate island in the Arctic Ocean. Sergei,'
            ' a seasoned meteorologist, and Pavel, a recent college graduate, '
            'are spending months in complete isolation on the once strategic '
            'research base. Pavel receives an important radio message and is '
            'still trying to find the right moment to tell Sergei, when fear, '
            'lies and suspicions start poisoning the atmosphere...'
        )]
        self.assertEqual(expected_plots, title.plots)

if __name__ == '__main__':
    unittest.main()
