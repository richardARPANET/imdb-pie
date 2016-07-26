from __future__ import absolute_import, unicode_literals

from operator import itemgetter

import pytest

from imdbpie.imdbpie import Title

from tests.utils import load_test_data


@pytest.fixture
def set_up():
    data = load_test_data('title_maindetails.json')
    title = Title(data=data)

    return {
        'title_data': data,
        'title': title
    }


def test_extract_trailers(set_up):
    title = set_up['title']
    data = set_up['title_data']

    trailers = title._extract_trailers(data)
    expected_trailers = [
        {
            'format': 'H.264 Fire 600',
            'url': (
                'http://video-http.media-imdb.com/'
                'MV5BNzcyNDc3ODY5OV5BMTFeQW1wNF5BbWU3MDY4Njc3OTY@.mp4'
                '?Expires=1425627377&Signature=3dACdpNTKNQH3JapQ7zCe0fHoRVxIT'
                'jDVi3on2VUZjkwyMtgbD2Zpx-xjxqc7-k214X73RLqJC-8G6c99Mxm4OTkps'
                'uw-HW2u0Xf~~Z~PcUCLuvevZBY5uJPNcng1BxmEzosN6h2~uspL7nlTWZMfy'
                'zC-NohkUONxVR5plYs65g_&Key-Pair-Id=APKAILW5I44IHKUN2DYA'
            )
        },
        {
            'format': 'iPhone 3G',
            'url': (
                'http://video-http.media-imdb.com/'
                'MV5BMTY2NzE2NDY4Ml5BMTFeQW1wNF5BbWU3MDQ1NTEyOTM@.mp4?Expires'
                '=1425627377&Signature=32Q7Qgp2rjsM~ul3mrZuielazFAt-5~y5JmzV'
                '4V9tRtvLjiH2LDPNhPg6z0YN96JeBiLCoI~YNHH5qRZucBcZ5Fd3ZKwL95z'
                '0oS0qo087cyOsV~Ke4d11k8A-twG5hHl9FjnjmUueC6SXedMbczETadurOZ'
                'AUBMenCO2aM4pvx0_&Key-Pair-Id=APKAILW5I44IHKUN2DYA'
            )
        }
    ]

    assert (
        sorted(expected_trailers, key=itemgetter('format')) ==
        sorted(trailers, key=itemgetter('format'))
    )


def test_extract_trailer_image_urls(set_up):
    title = set_up['title']
    data = set_up['title_data']

    expected_urls = [
        ('http://ia.media-imdb.com/images/M/'
         'MV5BMTg4NjMwOTY2Ml5BMl5BanBnXkFtZTcwMDY1MTI5Mw@@._V1_.jpg')
    ]

    urls = title._extract_trailer_image_urls(data)

    assert expected_urls == urls


def test_extract_creators(set_up):
    title = set_up['title']
    data = set_up['title_data']

    creators = title._extract_creators(data)

    assert 2 == len(creators)
    assert 'nm0001778' == creators[0].imdb_id
    assert 'Matt Stone' == creators[0].name
    assert 'nm0005295' == creators[1].imdb_id
    assert 'Trey Parker' == creators[1].name


def test_extract_directors_summary(set_up):
    title = set_up['title']
    data = set_up['title_data']

    directors_summary = title._extract_directors_summary(data)

    assert 1 == len(directors_summary)
    assert 'nm1403225' == directors_summary[0].imdb_id
    assert 'Aleksey Popogrebskiy' == directors_summary[0].name


def test_extract_cast_summary(set_up):
    title = set_up['title']
    data = set_up['title_data']

    cast_summary = title._extract_cast_summary(data)

    assert 4 == len(cast_summary)
    assert 'nm3732046' == cast_summary[0].imdb_id
    assert 'Grigoriy Dobrygin' == cast_summary[0].name
    assert 'nm1655234' == cast_summary[1].imdb_id
    assert 'Sergey Puskepalis' == cast_summary[1].name
    assert 'nm3778981' == cast_summary[3].imdb_id
    assert 'Artyom Tsukanov' == cast_summary[3].name


def test_extract_writers_summary(set_up):
    title = set_up['title']
    data = set_up['title_data']

    writers_summary = title._extract_writers_summary(data)

    assert 1 == len(writers_summary)
    assert 'nm1403225' == writers_summary[0].imdb_id
    assert 'Aleksey Popogrebskiy' == writers_summary[0].name


def test_extract_year(set_up):
    title = set_up['title']
    data = set_up['title_data']
    assert 2010 == title._extract_year(data)


def test_extract_year_no_year():
    data = {'year': '????'}
    title = Title(data=data)
    assert title._extract_year(data) is None


def test_extract_cover_url(set_up):
    title = set_up['title']
    data = set_up['title_data']

    expected_cover_url = (
        'http://ia.media-imdb.com/images/M/'
        'MV5BMTUyNjE5NTEzM15BMl5BanBnXkFtZTcwNjc0MTI5Mw@@'
        '._V1__SX214_.jpg'
    )
    cover_url = title._extract_cover_url(data)

    assert expected_cover_url == cover_url


def test_extract_credits():
    credits_data = load_test_data('title_maindetails.json')['credits']
    data = {'credits': credits_data[0:3]}

    title = Title(data=data)

    people = title._extract_credits(data)

    assert 6 == len(people)

    assert people[0].roles == []
    assert people[0].label == 'Directed by'
    assert people[0].token == 'directors'
    assert people[0].name == 'Aleksey Popogrebskiy'
    assert people[0].imdb_id == 'nm1403225'

    assert people[5].roles == ['Golos po ratsii - Volodya']
    assert people[5].label == 'Cast'
    assert people[5].token == 'cast'
    assert people[5].name == 'Ilya Sobolev'
    assert people[5].imdb_id == 'nm3777825'

    assert people[2].roles == ['Sergey']
    assert people[2].label == 'Cast'
    assert people[2].token == 'cast'
    assert people[2].name == 'Sergey Puskepalis'
    assert people[2].imdb_id == 'nm1655234'
