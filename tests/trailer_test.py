from imdbpie import Imdb
import unittest

imdb = Imdb({'anonymize': False})
movie = imdb.find_movie_by_id("tt0382932")


class TestTrailer(unittest.TestCase):

    def test_trailer_url(self):
        self.assertIsNotNone(movie.trailers)


if __name__ == '__main__':
    unittest.main()