from datetime import date

import pytest

from imdbpie import Imdb, ImdbFacade
from imdbpie.objects import TitleEpisode, Title, Name, TitleName


@pytest.fixture(scope='module')
def client():
    client = Imdb(locale='en_US')
    yield client
    client.clear_cached_credentials()


@pytest.fixture(scope='module')
def facade(client):
    return ImdbFacade(client=client)


def test_get_title_tv_show(facade):
    tv_show_imdb_id = 'tt0096697'
    title = facade.get_title(imdb_id=tv_show_imdb_id)

    assert isinstance(title, Title)
    _check_title(title=title, facade=facade)
    assert title.type == 'tvseries'

    assert str(title) == 'Title(imdb_id=tt0096697, title=The Simpsons)'

    num_checked = 0
    for episode in title.episodes:
        assert isinstance(episode, TitleEpisode)
        assert episode.imdb_id
        assert isinstance(episode.season, int)
        assert isinstance(episode.episode, int)
        _check_title(title=episode, facade=facade)
        num_checked += 1
        if num_checked > 5:
            break

    # Sequence operations
    assert title.episodes[0].season == 1
    assert title.episodes[0].episode == 1
    assert title.episodes
    assert len(title.episodes)
    assert title.episodes[-1].imdb_id
    assert title.episodes[10].imdb_id


def test_get_title_movie(facade):
    tv_show_imdb_id = 'tt0468569'
    title = facade.get_title(imdb_id=tv_show_imdb_id)
    assert isinstance(title, Title)
    _check_title(title=title, facade=facade)

    assert title.type == 'movie'
    assert len(title.episodes) == 0


@pytest.mark.parametrize('imdb_id', [
    'tt0795176',
    'tt7983794',
])
def test_get_title_documentary(facade, imdb_id):
    title = facade.get_title(imdb_id=imdb_id)

    assert isinstance(title, Title)
    _check_title(title=title, facade=facade)

    assert title.type in ('tvminiseries', 'movie')

    num_checked = 0
    for episode in title.episodes:
        assert episode
        assert episode.imdb_id
        assert isinstance(episode.season, int)
        assert isinstance(episode.episode, int)
        _check_title(title=episode, facade=facade)
        num_checked += 1
        if num_checked > 5:
            break


@pytest.mark.parametrize('imdb_id', [
    'nm0000151',
    'nm0588033',
    'nm0047800',
    'nm1799952',
])
def test_get_name(facade, imdb_id):
    name = facade.get_name(imdb_id=imdb_id)

    assert isinstance(name, Name)
    if name.image:
        assert isinstance(name.image.url, str)
        assert isinstance(name.image.width, int)
        assert isinstance(name.image.height, int)
    assert name.imdb_id == imdb_id
    assert isinstance(name.date_of_birth, date)
    assert isinstance(name.bios, tuple)
    assert name.gender in ('male', 'female')
    assert isinstance(name.birth_place, str)
    assert isinstance(name.name, str)
    for bio in name.bios:
        assert isinstance(bio, str)

    for imdb_id in name.filmography:
        facade._client.validate_imdb_id(imdb_id)


def test_get_title_episode(facade):
    episode_imdb_id = 'tt4847050'
    title = facade.get_title_episode(imdb_id=episode_imdb_id)

    assert isinstance(title, TitleEpisode)
    assert title.imdb_id == episode_imdb_id
    assert isinstance(title.season, int)
    assert isinstance(title.episode, int)


def test_search_for_name(facade):
    pass


def test_search_for_title(facade):
    pass


def _check_title(title, facade):
    assert isinstance(title.title, str)
    assert isinstance(title.type, str)
    assert isinstance(title.year, int)
    assert isinstance(title.rating_count, int)
    assert isinstance(title.rating, float)
    assert isinstance(title.release_date, date)
    if title.plot_outline:
        assert isinstance(title.plot_outline, str)

    assert title.releases
    for release in title.releases:
        assert isinstance(release.date, date)
        assert isinstance(release.region, str)

    assert isinstance(title.writers, tuple)
    for name in title.writers:
        assert isinstance(name, TitleName)
        assert isinstance(name.name, str)
        if name.job is not None:
            assert isinstance(name.job, str)
        assert isinstance(name.imdb_id, str)
        facade._client.validate_imdb_id(name.imdb_id)

    assert isinstance(title.creators, tuple)
    for name in title.creators:
        assert isinstance(name, TitleName)
        assert isinstance(name.name, str)
        assert name.job == 'creator'
        assert isinstance(name.imdb_id, str)
        facade._client.validate_imdb_id(name.imdb_id)

    assert isinstance(title.directors, tuple)
    for name in title.directors:
        assert isinstance(name, TitleName)
        assert isinstance(name.name, str)
        if name.job is not None:
            assert isinstance(name.job, str)
        assert isinstance(name.imdb_id, str)
        facade._client.validate_imdb_id(name.imdb_id)

    assert isinstance(title.credits, tuple)
    for name in title.credits:
        assert isinstance(name, TitleName)
        assert isinstance(name.name, str)
        if name.job is not None:
            assert isinstance(name.job, str)
        assert isinstance(name.imdb_id, str)
        facade._client.validate_imdb_id(name.imdb_id)

    assert isinstance(title.stars, tuple)
    for name in title.stars:
        assert isinstance(name.name, str)
        assert not name.job
        assert isinstance(name.characters, tuple)
        for character_name in name.characters:
            assert isinstance(character_name, str)
        assert name.category
        assert isinstance(name.imdb_id, str)
        facade._client.validate_imdb_id(name.imdb_id)

    assert isinstance(title.genres, tuple)
    for genre in title.genres:
        assert isinstance(genre, str)

    assert isinstance(title.certification, str)

    assert title.image
    assert isinstance(title.image.url, str)
    assert isinstance(title.image.width, int)
    assert isinstance(title.image.height, int)
