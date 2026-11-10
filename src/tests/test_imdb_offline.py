# coding: utf-8
from __future__ import absolute_import, unicode_literals

import pytest

from imdbpie import Imdb


@pytest.fixture(scope='module')
def client():
    client = Imdb(locale='en_US')
    yield client
    client.clear_cached_credentials()


def test_get_title_episodes_raises_when_exclude_episodes_enabled():
    client = Imdb(exclude_episodes=True)
    with pytest.raises(ValueError):
        client.get_title_episodes('tt0303461')


@pytest.mark.parametrize(
    'imdb_id, exp_valid',
    [
        ('tt1234567', True),
        ('nm1234567', True),
        ('x', False),
        (1234567, False),
        (None, False),
    ],
)
def test_validate_imdb_id(imdb_id, exp_valid, client):
    if exp_valid:
        # no raise
        client.validate_imdb_id(imdb_id)
    else:
        with pytest.raises(ValueError):
            client.validate_imdb_id(imdb_id)
