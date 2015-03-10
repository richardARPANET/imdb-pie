import pytest

from tests.utils import load_test_data
from imdbpie.objects import Image


@pytest.fixture
def set_up():
    data = load_test_data('title_maindetails.json')

    return {
        'data': data,
    }


def test_image(set_up):
    data = set_up['data']

    image = Image(data=data)

    expected_url = (
        'http://ia.media-imdb.com/images/M/'
        'MV5BMTUyNjE5NTEzM15BMl5BanBnXkFtZTcwNjc0MTI5Mw@@._V1_.jpg')

    assert image.caption is None
    assert expected_url == image.url
    assert 1455 == image.width
    assert 2048 == image.height
