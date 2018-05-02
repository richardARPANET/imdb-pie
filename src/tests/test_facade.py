from datetime import date

import pytest

from imdbpie import Imdb, ImdbFacade


@pytest.fixture(scope='module')
def client():
    client = Imdb(locale='en_US')
    yield client
    client.clear_cached_credentials()


@pytest.fixture(scope='module')
def facade(client):
    return ImdbFacade(client=client)


def test_init(facade):
    assert isinstance(facade, ImdbFacade)


def test_get_title(facade):
    title = facade.get_title(imdb_id='tt0096697')

    assert isinstance(title.title, str)
    assert isinstance(title.type, str)
    assert isinstance(title.year, int)
    assert isinstance(title.rating_count, int)
    assert isinstance(title.rating, float)
    assert isinstance(title.release_date, date)
    assert isinstance(title.plot_outline, str)

    assert title.releases
    for release in title.releases:
        assert isinstance(release.date, date)
        assert isinstance(release.region, str)

    assert title.writers
    for name in title.writers:
        assert isinstance(name.name, str)
        if name.job is not None:
            assert isinstance(name.job, str)
        assert isinstance(name.imdb_id, str)
        facade._client.validate_imdb_id(name.imdb_id)

    assert title.creators
    for name in title.creators:
        assert isinstance(name.name, str)
        assert name.job == 'creator'
        assert isinstance(name.imdb_id, str)
        facade._client.validate_imdb_id(name.imdb_id)

    assert title.directors
    for name in title.directors:
        assert isinstance(name.name, str)
        if name.job is not None:
            assert isinstance(name.job, str)
        assert isinstance(name.imdb_id, str)
        facade._client.validate_imdb_id(name.imdb_id)

    assert title.credits
    for name in title.credits:
        assert isinstance(name.name, str)
        if name.job is not None:
            assert isinstance(name.job, str)
        assert isinstance(name.imdb_id, str)
        facade._client.validate_imdb_id(name.imdb_id)

    assert title.genres
    for genre in title.genres:
        assert isinstance(genre, str)
    # assert isinstance(title.certification, str)
