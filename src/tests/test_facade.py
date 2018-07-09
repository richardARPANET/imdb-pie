from datetime import date

import pytest
import six

from imdbpie import ImdbFacade
from imdbpie.objects import (
    Title, Name, TitleName, TitleSearchResult, NameSearchResult
)


@pytest.fixture(scope='module')
def facade():
    return ImdbFacade()


class TestGetTitle(object):

    def test_tv_show(self, facade):
        tv_show_imdb_id = 'tt0096697'
        title = facade.get_title(imdb_id=tv_show_imdb_id)

        assert isinstance(title, Title)
        _check_title(title=title, facade=facade)
        assert title.type == 'tvseries'
        assert isinstance(title.runtime, int)
        assert title.runtime > 0

        num_checked = 0
        for episode in title.episodes:
            assert isinstance(episode, Title)
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

    @pytest.mark.parametrize('movie_imdb_id', [
        'tt0468569',
        'tt0017587',
    ])
    def test_movie(self, facade, movie_imdb_id):
        title = facade.get_title(imdb_id=movie_imdb_id)
        assert isinstance(title, Title)
        _check_title(title=title, facade=facade)
        assert title.type == 'movie'
        assert title.imdb_id == movie_imdb_id
        assert len(title.episodes) == 0
        assert isinstance(title.runtime, (int, type(None)))
        if title.runtime is not None:
            assert title.runtime > 0

    @pytest.mark.parametrize('imdb_id', [
        'tt0795176',
        'tt7983794',
    ])
    def test_get_title_documentary(self, facade, imdb_id):
        title = facade.get_title(imdb_id=imdb_id)

        assert isinstance(title, Title)
        _check_title(title=title, facade=facade)

        assert title.type in ('tvminiseries', 'movie')
        assert isinstance(title.runtime, int)
        assert title.runtime > 0

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

    @pytest.mark.parametrize('episode_imdb_id', [
        'tt4847050',
        'tt4849022',
    ])
    def test_tv_episode(self, facade, episode_imdb_id):
        title = facade.get_title(imdb_id=episode_imdb_id)

        assert isinstance(title, Title)

        assert isinstance(title.runtime, (int, type(None)))
        assert title.imdb_id == episode_imdb_id
        assert len(title.episodes) == 0
        assert isinstance(title.season, int)
        assert isinstance(title.episode, int)


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
        assert isinstance(name.image.url, six.string_types)
        assert isinstance(name.image.width, int)
        assert isinstance(name.image.height, int)
    assert name.imdb_id == imdb_id
    assert isinstance(name.date_of_birth, date)
    assert isinstance(name.bios, tuple)
    assert name.gender in ('male', 'female')
    assert isinstance(name.birth_place, six.string_types)
    assert isinstance(name.name, six.string_types)
    for bio in name.bios:
        assert isinstance(bio, six.string_types)

    for imdb_id in name.filmography:
        facade._client.validate_imdb_id(imdb_id)


def test_search_for_name(facade):
    results = facade.search_for_name('Tom Hanks')

    assert results
    for result in results:
        assert isinstance(result, NameSearchResult)
        assert result.imdb_id.startswith('nm')
        assert isinstance(result.name, six.string_types)


def test_search_for_title(facade):
    results = facade.search_for_title('The Dark Knight')

    assert results
    for result in results:
        assert isinstance(result, TitleSearchResult)
        assert result.imdb_id.startswith('tt')
        assert isinstance(result.title, six.string_types)
        if result.year:
            assert isinstance(result.year, int)


def _check_title(title, facade):
    assert isinstance(title.title, six.string_types)
    assert isinstance(title.type, six.string_types)
    assert isinstance(title.year, int)
    assert isinstance(title.rating_count, int)
    assert isinstance(title.rating, float)
    assert isinstance(title.release_date, date)
    if title.plot_outline:
        assert isinstance(title.plot_outline, six.string_types)

    assert title.releases
    for release in title.releases:
        assert isinstance(release.date, date)
        assert isinstance(release.region, six.string_types)

    assert isinstance(title.writers, tuple)
    for name in title.writers:
        assert isinstance(name, TitleName)
        assert isinstance(name.name, six.string_types)
        if name.job is not None:
            assert isinstance(name.job, six.string_types)
        assert isinstance(name.imdb_id, six.string_types)
        facade._client.validate_imdb_id(name.imdb_id)

    assert isinstance(title.creators, tuple)
    for name in title.creators:
        assert isinstance(name, TitleName)
        assert isinstance(name.name, six.string_types)
        assert name.job == 'creator'
        assert isinstance(name.imdb_id, six.string_types)
        facade._client.validate_imdb_id(name.imdb_id)

    assert isinstance(title.directors, tuple)
    for name in title.directors:
        assert isinstance(name, TitleName)
        assert isinstance(name.name, six.string_types)
        if name.job is not None:
            assert isinstance(name.job, six.string_types)
        assert isinstance(name.imdb_id, six.string_types)
        facade._client.validate_imdb_id(name.imdb_id)

    assert isinstance(title.credits, tuple)
    for name in title.credits:
        assert isinstance(name, TitleName)
        assert isinstance(name.name, six.string_types)
        if name.job is not None:
            assert isinstance(name.job, six.string_types)
        assert isinstance(name.imdb_id, six.string_types)
        facade._client.validate_imdb_id(name.imdb_id)

    assert isinstance(title.stars, tuple)
    for name in title.stars:
        assert isinstance(name.name, six.string_types)
        assert not name.job
        assert isinstance(name.characters, tuple)
        for character_name in name.characters:
            assert isinstance(character_name, six.string_types)
        assert name.category
        assert isinstance(name.imdb_id, six.string_types)
        facade._client.validate_imdb_id(name.imdb_id)

    assert isinstance(title.genres, tuple)
    for genre in title.genres:
        assert isinstance(genre, six.string_types)

    assert isinstance(title.certification, (six.string_types, type(None)))

    if title.image:
        assert isinstance(title.image.url, six.string_types)
        assert isinstance(title.image.width, int)
        assert isinstance(title.image.height, int)
