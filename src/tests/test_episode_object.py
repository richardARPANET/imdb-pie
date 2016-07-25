from __future__ import absolute_import, unicode_literals

import pytest

from imdbpie.objects import Episode

from tests.utils import load_test_data


@pytest.fixture
def set_up():
    data = load_test_data('title_episodes.json')

    seasons = data.get('data').get('seasons')
    first_episode = seasons[0].get('list')[0]
    first_episode['series_name'] = 'Some Series Name'
    first_episode['episode'] = 4
    first_episode['season'] = 5
    return {
        'data': first_episode,
    }


def test_episode(set_up):
    data = set_up['data']
    episode = Episode(data=data)

    assert episode.imdb_id == 'tt1001012'
    assert episode.type == 'tv_episode'
    assert episode.title == 'Who Can Gain the Most Weight in One Week?'
    assert episode.release_date == '2002'
    assert episode.season == 5
    assert episode.episode == 4
    assert episode.series_name == 'Some Series Name'
    assert episode.year == 2002


@pytest.mark.parametrize('value,expected', [
    ('unknown', None),
    ('100', 100),
    (10, 10),
    (None, None),
])
def test_extract_season_episode(value, expected):
    episode = Episode(data={})

    assert episode._extract_season_episode(value=value) == expected
