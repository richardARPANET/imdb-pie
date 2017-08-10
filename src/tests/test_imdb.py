# coding: utf-8
from __future__ import absolute_import, unicode_literals

import time
import datetime
from operator import itemgetter

import pytest
from mock import patch
from six.moves.urllib_parse import quote

from imdbpie import Imdb
from imdbpie.objects import Image, Person
from imdbpie.exceptions import HTTPError

from tests.utils import load_test_data, assert_urls_match, is_valid_url


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

        assert len(plots) >= 5
        assert expected_plot3 in plots

    def test_get_credits_data(self):
        credits = self.imdb._get_credits_data('tt0111161')
        expected_credits = load_test_data('get_credits_tt0111161.json')

        assert len(expected_credits) <= len(credits)
        for index, credit_item in enumerate(expected_credits):
            assert (
                sorted(credit_item, key=itemgetter(1)) ==
                sorted(credits[index], key=itemgetter(1))
            )

    def test_get_credits_non_existant_title(self):

        with pytest.raises(HTTPError):
            self.imdb._get_credits_data('tt-non-existant-id')

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

    def test_get_title_reviews_limit(self):
        reviews = self.imdb.get_title_reviews('tt2294629', max_results=20)
        assert 20 == len(reviews)

        reviews = self.imdb.get_title_reviews('tt2294629', max_results=31)
        assert 31 == len(reviews)

    def test_title_reviews_non_existant_title(self):

        with pytest.raises(HTTPError):
            self.imdb.get_title_reviews('tt-non-existant-id')

    def test_title_exists(self):
        result = self.imdb.title_exists('tt2322441')
        assert True is result

    def test_title_exists_non_existant_title(self):
        result = self.imdb.title_exists('tt0000000')
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

        assert 14 == len(results)
        assert expected_top_results == results[:2]

    def test_search_for_person(self):
        results = self.imdb.search_for_person('Andrew Lloyd Webber')

        assert 12 == len(results)
        expected_results = [
            {'name': 'Andrew Lloyd Webber', 'imdb_id': 'nm0515908'},
            {'name': 'Andrew Lloyd Walker', 'imdb_id': 'nm3530714'},
            {'name': 'Robert Lloyd', 'imdb_id': 'nm0516115'},
            {'name': 'Madeleine Gurdon', 'imdb_id': 'nm2967056'},
            {'name': 'Andrew Webberley', 'imdb_id': 'nm1422165'},
            {'name': 'Imogen Lloyd Webber', 'imdb_id': 'nm2622250'},
            {'name': 'Andrew Webber', 'imdb_id': 'nm8698321'},
            {'name': 'Robert Floyd', 'imdb_id': 'nm0283292'},
            {'name': 'Andrew Webber', 'imdb_id': 'nm0916341'},
            {'name': 'Andrew Webber', 'imdb_id': 'nm1267376'},
            {'name': 'Andrew Webber', 'imdb_id': 'nm3404464'},
            {'name': 'Mark Webber', 'imdb_id': 'nm1902514'}
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
            # 'image',  # optional key
            'year',
            'principals',
            'type'
        ]
        # results are changeable so check on data structure
        for index, result in enumerate(results):
            assert set(expected_keys).issubset(set(result.keys())) is True

    def test_popular_movies(self):
        results = self.imdb.popular_movies()

        assert 25 == len(results)

        expected_keys = [
            'tconst',
            'title',
            'year',
            'principals',
            'type'
        ]
        for index, result in enumerate(results):
            assert set(expected_keys).issubset(set(result['object'].keys())) is True

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
        assert is_valid_url(person.photo_url) is True

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
        assert len(title.plots) >= 5
        assert isinstance(title.rating, float) is True
        assert sorted(title.genres) == sorted(['Crime', 'Drama'])
        assert isinstance(title.votes, int) is True
        assert title.runtime == 8520

        assert is_valid_url(title.poster_url) is True
        assert is_valid_url(title.cover_url) is True
        assert title.release_date == '1994-10-14'
        assert title.certification == 'R'

        for trailer_url in title.trailer_image_urls:
            assert is_valid_url(trailer_url) is True

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

        assert len(title.credits) >= 327
        assert (
            sorted(load_test_data('expected_credits.json')) ==
            sorted([p.imdb_id for p in title.credits])
        )
        assert isinstance(title.credits[10], Person)

        assert len(title.trailers) == 3

    def test_get_title_by_id_using_proxy(self):
        imdb = Imdb(locale='en_US', cache=False, anonymize=True)
        title = imdb.get_title_by_id('tt0111161')

        assert title.title == 'The Shawshank Redemption'
        assert title.year == 1994
        assert title.type == 'feature'
        assert title.tagline == ('Fear can hold you prisoner. '
                                 'Hope can set you free.')
        assert isinstance(title.plots, list) is True
        assert len(title.plots) >= 5
        assert isinstance(title.rating, float) is True
        assert sorted(title.genres) == sorted(['Crime', 'Drama'])
        assert isinstance(title.votes, int) is True
        assert title.runtime == 8520
        assert len(title.trailers) == 3

    def test_get_title_by_id_redirection_result(self):
        assert self.imdb.get_title_by_id('tt0000021') is None

    def test_get_title_by_id_excludes_episodes(self):
        assert self.imdb.get_title_by_id('tt3181538') is not None

        imdb = Imdb(exclude_episodes=True)
        title = imdb.get_title_by_id('tt3181538')

        assert title is None

    def test_get_episodes(self):
        assert self.imdb.get_title_by_id('tt0303461') is not None

        imdb = Imdb()
        episodes = imdb.get_episodes('tt0303461')
        assert episodes is not None

        assert len(episodes) == 14
        episode_1 = episodes[0]
        assert episode_1.imdb_id == "tt0579539"
        assert episode_1.type == "tv_episode"
        assert episode_1.title == u'The Train Job'
        assert episode_1.series_name == 'Firefly'
        assert episode_1.release_date == "2002-09-20"
        assert episode_1.year == 2002

    def test_get_episodes_raises_when_exclude_episodes_enabled(self):
        imdb = Imdb(locale='en_US', cache=False, exclude_episodes=True)
        with pytest.raises(ValueError):
            imdb.get_episodes('tt0303461')

    def test_get_person_images(self):
        person_images = self.imdb.get_person_images('nm0000032')

        assert len(person_images) >= 200
        for person_image in person_images[:10]:
            assert person_image.caption is not None
            assert is_valid_url(person_image.url) is True
            assert isinstance(person_image.width, int)
            assert isinstance(person_image.height, int)

    def test_get_title_images(self):
        title_images = self.imdb.get_title_images('tt0111161')

        assert len(title_images) >= 38

        for image in title_images:
            assert isinstance(image, Image) is True

    def test_get_title_by_id_raises_not_found(self):

        with pytest.raises(HTTPError):
            self.imdb.get_title_by_id('tt9999999')
