from imdbpie import Imdb
try:
    import unittest2 as unittest  # for Python <= 2.6
except ImportError:
    import unittest

imdb = Imdb({'anonymize': False})
reviews = imdb.title_reviews(imdb_id="tt0468569", limit=3)


class TestTitleReviews(unittest.TestCase):

    def test_title_reviews(self):
        self.assertEqual(len(reviews), 3)

        expected_results = [
            {
                'user_name': 'straightblaster',
                'summary': 'Film surpasses the hype',
                'date': '2008-07-09'
            },
            {
                'user_name': 'johnnymacbest',
                'summary': 'Surpasses "Begins" in every aspect!!!',
                'date': '2008-07-07'
            },
            {
                'user_name': 'manuel_de_dios',
                'summary': 'Best movie of 2008 hands down!',
                'date': '2008-07-07'
            },
        ]

        for idx, result in enumerate(expected_results):
            self.assertEqual(result['user_name'], reviews[idx].username)
            self.assertEqual(result['summary'], reviews[idx].summary)
            self.assertEqual(result['date'], reviews[idx].date)
            self.assertIsNotNone(reviews[idx].text)
            self.assertIsNotNone(reviews[idx].status)
            self.assertIsNotNone(reviews[idx].user_score)
            self.assertIsNotNone(reviews[idx].user_score_count)
            self.assertIsNotNone(reviews[idx].user_location)
            self.assertIsNotNone(reviews[idx].date)

if __name__ == '__main__':
    unittest.main()
