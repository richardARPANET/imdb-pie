from __future__ import absolute_import, unicode_literals

import cgi
import time
import datetime
from operator import itemgetter

import pytest
from six.moves.urllib_parse import urlparse, quote

from mock import patch
from imdbpie import Imdb
from imdbpie.objects import Image, Person, Review

from tests.utils import load_test_data, assert_urls_match


class TestImdb(object):

    imdb = Imdb(locale='en_US', cache=False)

    def test_build_url(self):
        imdb_fr = Imdb(locale='en_FR', cache=False)
        imdb_fr.timestamp = time.mktime(datetime.date.today().timetuple())

        url = imdb_fr._build_url(
            path='/title/maindetails', params={'tconst': 'tt1111111'})

        expected_url = (
            'https://app.imdb.com/'
            'title/maindetails'
            '?apiKey=d2bb34ec6f6d4ef3703c9b0c36c4791ef8b9ca9b'
            '&apiPolicy=app1_1'
            '&locale=en_FR'
            '&timestamp={timestamp}'
            '&tconst=tt1111111&api=v1&appid=iphone1_1'
        ).format(timestamp=imdb_fr.timestamp)

        assert_urls_match(expected_url, url)

    def test_build_url_proxied(self):
        imdb_fr = Imdb(
            locale='en_FR',
            cache=False,
            anonymize=True,
            proxy_uri='http://someproxywebsite.co.uk?url={0}'
        )
        imdb_fr.timestamp = time.mktime(datetime.date.today().timetuple())

        url = imdb_fr._build_url(
            path='/title/maindetails', params={'tconst': 'tt1111111'})

        expected_url = (
            'http://someproxywebsite.co.uk?url=' +
            quote('https://app.imdb.com/title/maindetails')
        )
        assert url.startswith(expected_url) is True

    def test_get_title_plots(self):
        plots = self.imdb.get_title_plots('tt0111161')

        expected_plot0 = ('Andy Dufresne is a young and successful banker '
                          'whose life changes drastically when he is convicted'
                          ' and sentenced to life imprisonment for the murder '
                          'of his wife and her lover. Set in the 1940\'s, the '
                          'film shows how Andy, with the help of his friend '
                          'Red, the prison entrepreneur, turns out to be a '
                          'most unconventional prisoner.')
        expected_plot3 = ('Andy Dufresne is sent to Shawshank Prison for the '
                          'murder of his wife and her secret lover. He is very'
                          ' isolated and lonely at first, but realizes there '
                          'is something deep inside your body that people '
                          'can\'t touch or get to....\'HOPE\'. Andy becomes '
                          'friends with prison \'fixer\' Red, and Andy '
                          'epitomizes why it is crucial to have dreams. His '
                          'spirit and determination lead us into a world full '
                          'of imagination, one filled with courage and desire.'
                          ' Will Andy ever realize his dreams?')
        expected_plot4 = ('Bank Merchant Andy Defrene is convicted of the '
                          'murder of his wife and her lover, and sentenced to '
                          'life imprisonment at Shawshank prison. Life seems '
                          'to have taken a turn for the worse, but fortunately'
                          ' Andy befriends some of the other inmates, in '
                          'particular a character known only as Red. Over time'
                          ' Andy finds ways to live out life with relative '
                          'ease as one can in a prison, leaving a message for'
                          ' all that while the body may be locked away in a '
                          'cell, the spirit can never be truly imprisoned.')

        assert 5 == len(plots)
        assert expected_plot0 == plots[0]
        assert expected_plot3 == plots[3]
        assert expected_plot4 == plots[4]

    def test_get_credits_data(self):
        credits = self.imdb._get_credits_data('tt0111161')
        expected_credits = load_test_data('get_credits_tt0111161.json')

        assert len(expected_credits) == len(credits)
        for index, credit_item in enumerate(expected_credits):
            assert (
                sorted(credit_item, key=itemgetter(1)) ==
                sorted(credits[index], key=itemgetter(1))
            )

    def test_get_credits_non_existant_title(self):
        credits = self.imdb._get_credits_data('tt-non-existant-id')
        assert credits is None

    def test_get_reviews_data(self):
        reviews = self.imdb._get_reviews_data('tt0111161')
        assert len(reviews) == 10

        expected_review_keys = [
            'status',
            'user_score',
            'text',
            'summary',
            'user_score_count',
            'date',
            'user_name'
        ]
        # other optional keys: user_rating, user_location

        # results are changeable so check on data structure
        for review in reviews:
            for key in expected_review_keys:
                assert key in review.keys()

    def test_get_title_reviews(self):
        reviews = self.imdb.get_title_reviews('tt0111161')
        assert 10 == len(reviews)

        assert reviews[0].username == 'carflo'
        assert reviews[0].date == '2003-11-26'
        assert reviews[0].summary == 'Tied for the best movie I have ever seen'

    def test_title_reviews_non_existant_title(self):
        assert self.imdb.get_title_reviews('tt-non-existant-id') is None

    def test_title_exists(self):
        result = self.imdb.title_exists('tt2322441')
        assert True is result

    def test_title_exists_non_existant_title(self):
        result = self.imdb.title_exists('tt-non-existant-id')
        assert False is result

    def test_search_for_title_searching_title(self):
        results = self.imdb.search_for_title('Shawshank redemption')
        expected_top_results = [
            {
                'imdb_id': 'tt0111161',
                'title': 'The Shawshank Redemption',
                'year': '1994'
            },
            {
                'imdb_id': 'tt0265738',
                'title': 'The SharkTank Redemption',
                'year': '2000'
            },
        ]

        assert 12 == len(results)
        assert expected_top_results == results[:2]

    def test_search_for_person(self):
        results = self.imdb.search_for_person('Brad Pitt')

        assert 17 == len(results)
        expected_results = [
            {'imdb_id': 'nm0000093', 'name': 'Brad Pitt'},
            {'imdb_id': 'nm6221785', 'name': 'Brad Pittance'},
            {'imdb_id': 'nm2876601', 'name': 'Brad Spitt'},
            {'imdb_id': 'nm2542384', 'name': 'Brad Witt'},
            {'imdb_id': 'nm7062918', 'name': 'Brad Pitz'},
            {'imdb_id': 'nm3258729', 'name': 'Bradd Spitt'},
            {'imdb_id': 'nm6173397', 'name': 'Brad Fitt'},
            {'imdb_id': 'nm1694695', 'name': 'Prad Pitt'},
            {'imdb_id': 'nm1784745', 'name': 'Brad Patton'},
            {'imdb_id': 'nm2296458', 'name': 'Brad Pattison'},
            {'imdb_id': 'nm6275510', 'name': 'Brad Sitton'},
            {'imdb_id': 'nm1583570', 'name': 'Brad Pitre'},
            {'imdb_id': 'nm4463090', 'name': 'Brad Patterson'},
            {'imdb_id': 'nm1899342', 'name': 'Brad Pattullo'},
            {'imdb_id': 'nm5741181', 'name': 'Brad Little'},
            {'imdb_id': 'nm1736569', 'name': 'Brad Potts'},
            {'imdb_id': 'nm2703988', 'name': 'Brad Pitt vom Mahdenwald'}
        ]
        assert (sorted(expected_results, key=itemgetter('imdb_id')) ==
                sorted(results, key=itemgetter('imdb_id')))

    def test_search_for_title_no_results(self):
        results = self.imdb.search_for_title('898582da396c93d5589e0')
        assert [] == results

    def test_top_250(self):
        results = self.imdb.top_250()

        assert 250 == len(results)

        expected_keys = [
            'rating',
            'tconst',
            'title',
            'image',
            'num_votes',
            'year',
            'can_rate',
            'type'
        ]
        # results are changeable so check on data structure
        for result in results:
            assert sorted(expected_keys) == sorted(result.keys())

    def test_popular_shows(self):
        results = self.imdb.popular_shows()

        assert 50 == len(results)

        expected_keys = [
            'tconst',
            'title',
            'image',
            'year',
            'principals',
            'type'
        ]
        # results are changeable so check on data structure
        for result in results:
            assert sorted(expected_keys) == sorted(result.keys())

    def test_get_title_by_id_returns_none_when_is_episode(self):
        imdb = Imdb(exclude_episodes=True)
        assert imdb.get_title_by_id('tt0615090') is None

    @patch('imdbpie.imdbpie.Imdb._get')
    def test_get_title_by_id_returns_none_when_no_resp(self, mock_get):
        mock_get.return_value = None
        assert self.imdb.get_title_by_id('tt0111161') is None

    def test_get_person_by_id(self):
        person = self.imdb.get_person_by_id('nm0000151')

        assert person.name == 'Morgan Freeman'
        assert person.imdb_id == 'nm0000151'

    @patch('imdbpie.imdbpie.Imdb._get')
    def test_get_person_by_id_returns_none_when_no_resp(self, mock_get):
        mock_get.return_value = None
        assert self.imdb.get_person_by_id('nm0000151') is None

    def test_get_title_by_id(self):
        title = self.imdb.get_title_by_id('tt0111161')

        assert title.title == 'The Shawshank Redemption'
        assert title.year == 1994
        assert title.type == 'feature'
        assert title.tagline == ('Fear can hold you prisoner. '
                                 'Hope can set you free.')
        assert isinstance(title.plots, list) is True
        assert len(title.plots) == 5
        assert isinstance(title.rating, float) is True
        assert sorted(title.genres) == sorted(['Crime', 'Drama'])
        assert isinstance(title.votes, int) is True
        assert title.runtime == 8520
        assert title.poster_url == (
            'http://ia.media-imdb.com/images/M/MV5BODU4MjU4NjIwNl5BMl5BanBnX'
            'kFtZTgwMDU2MjEyMDE@._V1_.jpg'
        )
        assert title.cover_url == (
            'http://ia.media-imdb.com/images/M/MV5BODU4MjU4NjIwNl5BMl5BanBnX'
            'kFtZTgwMDU2MjEyMDE@._V1__SX214_.jpg'
        )
        assert title.release_date == '1994-10-14'
        assert title.certification == 'R'
        assert title.trailer_image_urls == [
            'http://ia.media-imdb.com/images/M/MV5BMzAzMDI1MTE0MF5BMl5BanBnX'
            'kFtZTgwNjMxNTMzMzE@._V1_.jpg'
        ]
        expected_plot_outline = (
            'Two imprisoned men bond over a number '
            'of years, finding solace and eventual redemption through acts '
            'of common decency.'
        )
        assert title.plot_outline == expected_plot_outline

        assert isinstance(title.directors_summary[0], Person)
        assert len(title.directors_summary) == 1

        assert len(title.creators) == 0
        assert len(title.cast_summary) == 4

        expected_cast_names = ['Tim Robbins', 'Morgan Freeman',
                               'Bob Gunton', 'William Sadler']
        for name in expected_cast_names:
            assert name in [p.name for p in title.cast_summary]

        expected_writers = ['Stephen King', 'Frank Darabont']
        for name in expected_writers:
            assert name in [p.name for p in title.writers_summary]

        assert len(title.credits) == 325
        assert (
            sorted(load_test_data('expected_credits.json')) ==
            sorted([p.imdb_id for p in title.credits])
        )
        assert isinstance(title.credits[10], Person)

        assert len(title.trailers) == 3

    def test_get_title_by_id_redirection_result(self):
        assert self.imdb.get_title_by_id('tt0000021') is None

    def test_get_title_by_id_excludes_episodes(self):
        assert self.imdb.get_title_by_id('tt3181538') is not None

        imdb = Imdb(exclude_episodes=True)
        title = imdb.get_title_by_id('tt3181538')

        assert title is None

    def test_get_person_images(self):
        person_images = self.imdb.get_person_images('nm0000033')

        assert len(person_images) == 280
        assert person_images[0].caption == 'Alfred Hitchcock'
        assert person_images[0].url == (
            'http://ia.media-imdb.com/images/M/MV5BMTQwMzIzNDY0OV5BMl5BanBnX'
            'kFtZTcwMTg0MzgyOQ@@._V1_.jpg')
        assert person_images[0].width == 1308
        assert person_images[0].height == 2048

    def test_get_title_images(self):
        title_images = self.imdb.get_title_images('tt0111161')

        assert len(title_images) == 33

        for image in title_images:
            assert isinstance(image, Image) is True
