from imdbpie import Imdb
import unittest

imdb = Imdb({'anonymize': False})
movie = imdb.find_movie_by_id("tt0382932")


class TestPerson(unittest.TestCase):

    def test_name(self):
        self.assertIsNotNone(movie.credits)

    def test_director(self):
        self.assertEqual(movie.directors_summary[0].name, 'Brad Bird')

    def test_director_role(self):
        self.assertFalse(movie.directors_summary[0].role)

    def test_writers(self):
        self.assertEqual(movie.writers_summary[0].name, 'Brad Bird')

    def test_writers_role(self):
        self.assertFalse(movie.writers_summary[0].role)

if __name__ == '__main__':
    unittest.main()
