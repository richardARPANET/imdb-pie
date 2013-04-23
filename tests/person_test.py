import unittest
from imdbpie import Imdb

imdb = Imdb({'anonymize': False})
movie = imdb.find_movie_by_id("tt0382932")


class TestPerson(unittest.TestCase):

    def test_name(self):
        self.assertIsNotNone(movie.credits[0].name)

    def test_role(self):
        self.assertIsNotNone(movie.credits[0].role)

    def test_director(self):
        self.assertEqual(movie.directors[0].name, 'Brad Bird')

    def test_director_role(self):
        self.assertFalse(movie.directors[0].role)

    def test_writers(self):
        self.assertEqual(movie.writers[0].name, 'Brad Bird')

    def test_writers_role(self):
        self.assertFalse(movie.writers[0].role)

if __name__ == '__main__':
    unittest.main()