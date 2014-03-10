from imdbpie import Imdb
import unittest

imdb = Imdb({'anonymize': False})
images = imdb.title_images("tt0468569")


class TestImage(unittest.TestCase):

    def test_results(self):
        self.assertGreaterEqual(len(images), 107)

    def test_caption(self):
        self.assertEqual(images[0].caption, 'Still of Gary Oldman in The Dark Knight')

    def test_url(self):
        self.assertEqual(
            images[0].url,
            'http://ia.media-imdb.com/images/M/MV5BOTAxNzI0ND'
            'E1NF5BMl5BanBnXkFtZTcwNjczMTk2Mw@@._V1_.jpg')

if __name__ == '__main__':
    unittest.main()
