import pytest

from tests.utils import load_test_data
from imdbpie.objects import Review
from imdbpie import Imdb


@pytest.fixture
def set_up():
    pass


def test_review(set_up):
    imdb = Imdb({
        'locale': 'en_US',
        'cache': False
    })

    reviews_data = imdb._get_reviews('tt0111161')
    review = Review(data=reviews_data[0])

    assert 'carflo' == review.username
    assert review.text.startswith('Why do I want to write the 234th ') is True
    assert review.text.endswith('Redemption to touch the soul.') is True
    assert '2003-11-26' == review.date
    assert 10 == review.rating
    assert 'Tied for the best movie I have ever seen' == review.summary
    assert 'G' == review.status
    assert 'Texas' == review.user_location
    assert 1902 == review.user_score
    assert 2207 == review.user_score_count
