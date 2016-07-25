from __future__ import absolute_import, unicode_literals

import pytest

from imdbpie.objects import Episode

from tests.utils import load_test_data


@pytest.fixture
def set_up():
    data = load_test_data('title_episodes.json')

    seasons = data.get('data').get('seasons')
    first_episode = seasons[0].get('list')[0]

    return {
        'data': first_episode,
    }


def test_episode(set_up):
    data = set_up['data']

    episode = Episode(data=data)

    assert episode.imdb_id == 'tt0579539'
    assert episode.type == 'tv_episode'
    assert episode.title == u'The Train Job'
    assert episode.release_date == '2002-09-20'
    assert episode.year == 2002
