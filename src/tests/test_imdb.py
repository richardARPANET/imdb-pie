# coding: utf-8
from __future__ import absolute_import, unicode_literals

from operator import itemgetter

import pytest

from imdbpie import Imdb


@pytest.fixture(scope='module')
def client():
    client = Imdb(locale='en_US')
    yield client
    client.clear_cached_credentials()


def test_get_title_plot_synopsis(client):
    expected_keys = [
        '@type',
        'id',
        'plotSynopses',
        'title',
        'titleType',
        'year',
    ]

    resource = client.get_title_plot_synopsis('tt0111161')

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_plot(client):
    expected_keys = ['@type', 'outline', 'summaries', 'totalSummaries']

    resource = client.get_title_plot('tt0111161')

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_user_reviews(client):
    expected_keys = [
        '@type',
        'base',
        'paginationKey',
        'reviews',
        'totalReviews',
    ]

    resource = client.get_title_user_reviews('tt0111161')

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_metacritic_reviews(client):
    expected_keys = [
        '@type',
        'id',
        'metaScore',
        'metacriticUrl',
        'reviewCount',
        'userRatingCount',
        'userScore',
        'reviews',
        'title',
    ]

    resource = client.get_title_metacritic_reviews('tt0111161')

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_title_reviews_non_existant_title(client):
    with pytest.raises(LookupError):
        client.get_title_user_reviews('tt9999999')


def test_title_exists(client):
    result = client.title_exists('tt2322441')
    assert True is result


def test_title_exists_non_existant_title(client):
    result = client.title_exists('tt0000000')
    assert False is result


def test_search_for_title_searching_title(client):
    results = client.search_for_title('Shawshank redemption')
    expected_result = {
        'imdb_id': 'tt0111161',
        'title': 'The Shawshank Redemption',
        'year': '1994',
        'type': 'feature',
    }
    assert len(results) > 0
    assert expected_result in results


def test_search_for_title_returns_no_results_if_name_query(client):
    results = client.search_for_title('Grigoriy Dobrygin')
    assert len(results) == 0


@pytest.mark.parametrize(
    'query',
    [
        'Mission: Impossible',
        'Honey, I Shrunk the Kids',
        '4.3.2.1. (2010)',
        '500 Days of Summer (2009)',
        '$9.99 (2008)',
        'Goonies 1986',
        '[REC] (2007)',
        '[REC]² (2009)',
        '[REC]³ Genesis (2012)',
        '¡Three Amigos! (1986)',
        '(Untitled) (2009)',
        'Æon Flux(2005)',
    ],
)
def test_search_for_title_input_with_special_chars(query, client):
    results = client.search_for_title(query)
    assert len(results) > 0


def test_search_for_name(client):
    results = client.search_for_name('Andrew Lloyd Webber')

    assert len(results) > 0
    expected_results = [
        {'name': 'Andrew Lloyd Webber', 'imdb_id': 'nm0515908'},
    ]
    assert sorted(expected_results, key=itemgetter('imdb_id')) == sorted(
        results, key=itemgetter('imdb_id')
    )


def test_search_for_name_returns_no_results_if_title_query(client):
    results = client.search_for_name('Mission Impossible')
    assert len(results) == 0


def test_search_for_title_no_results(client):
    results = client.search_for_title('898582da396c93d5589e0')
    assert [] == results


def test_get_popular_titles(client):
    expected_keys = ['@type', 'id', 'ranks']

    resource = client.get_popular_titles()

    assert sorted(resource.keys()) == sorted(expected_keys)
    assert len(resource['ranks']) == 100


def test_get_popular_shows(client):
    expected_keys = ['@type', 'id', 'ranks']

    resource = client.get_popular_shows()

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_popular_movies(client):
    expected_keys = ['@type', 'id', 'ranks']

    resource = client.get_popular_movies()

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_name(client):
    expected_keys = [
        '@type',
        'base',
        'id',
        'jobs',
        'knownFor',
        'quotes',
        'trivia',
    ]

    resource = client.get_name('nm0000151')

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_name_filmography(client):
    expected_keys = ['@type', 'filmography']

    resource = client.get_name_filmography('nm0000151')

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title(client):
    imdb_id = 'tt0111161'
    expected_keys = [
        '@type',
        'base',
        'filmingLocations',
        'metacriticScore',
        'plot',
        'ratings',
        'similarities',
        'soundtrack',
    ]

    resource = client.get_title(imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_genres(client):
    imdb_id = 'tt0111161'
    expected_keys = ['@type', 'genres', 'id', 'title', 'titleType', 'year']

    resource = client.get_title_genres(imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_similarities(client):
    imdb_id = 'tt0111161'
    expected_keys = ['@type', 'base', 'id', 'similarities']

    resource = client.get_title_similarities(imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_awards(client):
    imdb_id = 'tt0111161'
    expected_keys = ['@type', 'awards', 'id']

    resource = client.get_title_awards(imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_releases(client):
    imdb_id = 'tt0111161'
    expected_keys = ['@type', 'releases', 'id', 'title', 'titleType', 'year']

    resource = client.get_title_releases(imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_auxiliary(client):
    imdb_id = 'tt0111161'
    expected_keys = [
        'certificate',
        'filmingLocations',
        'metacriticInfo',
        'plot',
        'principals',
        'rating',
        'numberOfVotes',
        'canRate',
        'topRank',
        'userRating',
        'alternateTitlesSample',
        'alternateTitlesCount',
        'hasAlternateVersions',
        'originalTitle',
        'runningTimes',
        'spokenLanguages',
        'origins',
        'similaritiesCount',
        'releaseDetails',
        'soundtracks',
        'genres',
        'reviewsTeaser',
        'reviewsCount',
        'hasContentGuide',
        'hasSynopsis',
        'hasCriticsReviews',
        'criticsReviewers',
        'crazyCreditsTeaser',
        'awards',
        'photos',
        'heroImages',
        'seasonsInfo',
        'productionStatus',
        'directors',
        'writers',
        'videos',
        'adWidgets',
        'id',
        'image',
        'runningTimeInMinutes',
        'title',
        'titleType',
        'year',
    ]

    resource = client.get_title_auxiliary(imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_auxiliary_raises_when_exclude_episodes_enabled():
    client = Imdb(exclude_episodes=True)
    episode_imdb_id = 'tt3181538'
    with pytest.raises(LookupError):
        client.get_title_auxiliary(episode_imdb_id)


def test_get_title_versions(client):
    imdb_id = 'tt0111161'
    expected_keys = [
        '@type',
        'alternateTitles',
        'alternateVersions',
        'colorations',
        'defaultTitle',
        'silent',
        'spokenLanguages',
        'originalTitle',
        'origins',
        'runningTimes',
        'id',
        'title',
        'titleType',
        'year',
    ]

    resource = client.get_title_versions(imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_ratings(client):
    imdb_id = 'tt0111161'
    expected_keys = [
        '@type',
        'id',
        'title',
        'titleType',
        'year',
        'bottomRank',
        'canRate',
        'rating',
        'ratingCount',
        'topRank',
    ]

    resource = client.get_title_ratings(imdb_id)

    assert set(expected_keys).issubset(resource.keys())


def test_get_title_quotes(client):
    imdb_id = 'tt0111161'
    expected_keys = ['@type', 'quotes', 'id', 'title', 'titleType', 'year']

    resource = client.get_title_quotes(imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_connections(client):
    imdb_id = 'tt0111161'
    expected_keys = ['@type', 'base', 'connections']

    resource = client.get_title_connections(imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_credits(client):
    imdb_id = 'tt0111161'
    expected_keys = ['@type', 'base', 'creditsSummary', 'id', 'credits']

    resource = client.get_title_credits(imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


@pytest.mark.xfail
def test_get_title_credits_with_redirection_result(client):
    redir_imdb_id = 'tt0000021'

    with pytest.raises(LookupError):
        client.get_title_credits(redir_imdb_id)


@pytest.mark.xfail
def test_get_title_redirection_result(client):
    redir_imdb_id = 'tt0000021'

    with pytest.raises(LookupError):
        client.get_title(redir_imdb_id)


def test_get_title_excludes_episodes(client):
    episode_imdb_id = 'tt3181538'
    assert client.get_title(episode_imdb_id) is not None

    with pytest.raises(LookupError) as exc:
        Imdb(exclude_episodes=True).get_title(episode_imdb_id)

    exc.match(r'Title not found. Title was an episode.+')


def test_get_title_episodes(client):
    tv_show_imdb_id = 'tt0303461'
    expected_keys = ['@type', 'base', 'id', 'seasons']

    resource = client.get_title_episodes(tv_show_imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_episodes_raises_when_exclude_episodes_enabled():
    client = Imdb(exclude_episodes=True)
    with pytest.raises(ValueError):
        client.get_title_episodes('tt0303461')


def test_get_title_episodes_raises_imdb_id_is_not_that_of_a_tv_show(client):
    non_show_imdb_id = 'tt0468569'
    with pytest.raises(LookupError):
        client.get_title_episodes(non_show_imdb_id)


@pytest.mark.parametrize(
    'params, exp_num_episodes, exp_episodes_total, exp_seasons',
    [
        # firefly
        (
            dict(imdb_id='tt0303461', offset=0, limit=500, season=1),
            14,
            14,
            [1],
        ),
        # Breaking bad
        (
            dict(imdb_id='tt0903747', offset=1, limit=6, season=4),
            5,
            13,
            [1, 2, 3, 4, 5],
        ),
    ],
)
def test_get_title_episodes_detailed(
    params, client, exp_num_episodes, exp_episodes_total, exp_seasons
):
    expected_keys = [
        'allSeasons',
        'end',
        'episodes',
        'region',
        'season',
        'seriesTitle',
        'start',
        'totalEpisodes',
    ]
    resource = client.get_title_episodes_detailed(**params)

    assert sorted(resource.keys()) == sorted(expected_keys)
    assert len(resource['episodes']) == exp_num_episodes
    assert resource['totalEpisodes'] == exp_episodes_total
    assert resource['allSeasons'] == exp_seasons


def test_get_title_top_crew(client):
    tv_show_imdb_id = 'tt0303461'
    expected_keys = ['directors', 'writers']

    resource = client.get_title_top_crew(tv_show_imdb_id)

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_name_images(client):
    expected_keys = ['@type', 'images', 'totalImageCount']

    resource = client.get_name_images('nm0000032')

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_name_videos(client):
    expected_keys = [
        '@type',
        'akas',
        'id',
        'image',
        'legacyNameText',
        'name',
        'size',
        'videoCounts',
        'videos',
    ]

    resource = client.get_name_videos('nm0000032')

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_images(client):
    expected_keys = ['@type', 'images', 'totalImageCount']

    resource = client.get_title_images('tt0111161')

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_videos(client):
    expected_keys = [
        '@type',
        'id',
        'image',
        'size',
        'title',
        'titleType',
        'videoCounts',
        'videos',
        'year',
    ]

    resource = client.get_title_videos('tt0111161')

    assert sorted(resource.keys()) == sorted(expected_keys)


def test_get_title_raises_not_found(client):
    with pytest.raises(LookupError):
        client.get_title('tt9999999')


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
