# coding: utf-8
from __future__ import absolute_import, unicode_literals

import pytest
import responses

from imdbpie import Imdb, ImdbFacade
from imdbpie.constants import BASE_URI
from imdbpie.objects import (
    Award,
    FilmingLocation,
    Name,
    Title,
    TitleBusiness,
    TitleCertificate,
    TitleName,
    TitleVideo,
    WatchOption,
)

CREDENTIALS_URL = (
    'https://api.imdbws.com/authentication/credentials/temporary/ios82'
)
TITLE_AUXILIARY_URL = (
    'https://api.imdbws.com/template/imdb-ios-writable/'
    'title-auxiliary-v31.jstl/render'
)
TOP_CREW_URL = (
    'https://api.imdbws.com/template/imdb-android-writable/'
    '7.3.top-crew.jstl/render'
)

CREDENTIALS = {
    'resource': {
        'accessKeyId': 'ASIAEXAMPLE',
        'secretAccessKey': 'secret',
        'sessionToken': 'session',
        'expirationTimeStamp': '2099-01-01T00:00:00Z',
    }
}

TITLE_AUXILIARY = {
    'id': '/title/tt0111161/',
    'title': 'The Shawshank Redemption',
    'titleType': 'movie',
    'year': 1994,
    'certificate': {
        'certificate': 'R',
        'ratingReason': 'Rated R for language and prison violence',
    },
    'genres': ['Drama'],
    'runningTimes': [{'timeMinutes': 142}],
    'principals': [
        {
            'id': '/name/nm0000209/',
            'name': 'Tim Robbins',
            'category': 'actor',
            'characters': ['Andy Dufresne'],
        }
    ],
    'image': {
        'url': 'https://m.media-amazon.com/images/poster.jpg',
        'height': 1800,
        'width': 1200,
    },
    'spokenLanguages': ['en'],
    'origins': ['US'],
    'alternateTitlesSample': ['Il buono'],
    'alternateTitlesCount': 1,
    'topRank': {'rank': 1, 'rankType': 'topMovies'},
    'metacriticInfo': {'metaScore': 82},
    'awards': {'awardsSummary': {'otherWinsCount': 21}},
    'productionStatus': {'status': 'released'},
    'videos': {
        'totalVideoCount': 1,
        'mainTrailer': {
            'contentType': 'Trailer',
            'description': 'Two imprisoned men bond.',
            'durationSeconds': 131,
            'encodings': [{'play': 'https://video.example/movie.m3u8'}],
        },
    },
}

TITLE_RESOURCE = {
    'base': {
        'id': '/title/tt0111161/',
        'title': 'The Shawshank Redemption',
        'titleType': 'movie',
        'year': 1994,
    },
    'ratings': {'rating': 9.3, 'ratingCount': 3263412},
    'plot': {'outline': {'text': 'Two imprisoned men bond.'}},
}

TOP_CREW = {
    'directors': [
        {
            'id': '/name/nm0001104/',
            'name': 'Frank Darabont',
            'category': 'director',
        }
    ],
    'writers': [
        {
            'id': '/name/nm0000175/',
            'name': 'Stephen King',
            'category': 'writer',
            'job': 'creator',
        }
    ],
}

FULL_CREDITS = {
    'credits': {
        'actor': [
            {
                'id': '/name/nm0000209/',
                'name': 'Tim Robbins',
                'category': 'actor',
            }
        ]
    }
}

RELEASES = {'releases': [{'date': '1994-10-14', 'region': 'US'}]}


def r(payload):
    """Wrap a payload in the ``resource`` envelope the client unwraps."""
    return {'resource': payload}


def add(mocked, path, payload):
    mocked.add(responses.GET, BASE_URI + path, json=r(payload))


def name_payload(imdb_id, missing=()):
    base = {
        'id': '/name/{0}/'.format(imdb_id),
        'name': 'A Person',
        'birthDate': '1958-10-16',
        'birthPlace': 'West Covina, California, USA',
        'gender': 'male',
        'heightCentimeters': 195.58,
        'realName': 'A Real Name',
        'image': {
            'url': 'https://m.media-amazon.com/images/person.jpg',
            'height': 400,
            'width': 311,
        },
    }
    for key in missing:
        base.pop(key)
    return {
        'base': base,
        'jobs': ['actor'],
        'knownFor': [{'id': '/title/tt0327056/', 'title': 'Mystic River'}],
        'quotes': [],
        'trivia': [],
    }


@pytest.fixture
def client(tmp_path):
    client = Imdb()
    client._cachedir = str(tmp_path)
    client.clear_cached_credentials()
    client.clear_cache()
    return client


@pytest.fixture
def facade(client):
    return ImdbFacade(client=client)


@pytest.fixture
def mocked():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.POST, CREDENTIALS_URL, json=CREDENTIALS)
        rsps.add(responses.GET, TITLE_AUXILIARY_URL, json=TITLE_AUXILIARY)
        rsps.add(responses.GET, TOP_CREW_URL, json=TOP_CREW)
        add(rsps, '/title/tt0111161/auxiliary', TITLE_RESOURCE)
        add(rsps, '/title/tt0111161/fullcredits', FULL_CREDITS)
        add(rsps, '/title/tt0111161/releases', RELEASES)
        add(rsps, '/name/nm0000209/fulldetails', name_payload('nm0000209'))
        rsps.add(
            responses.GET,
            BASE_URI + '/title/tt0111161/episodes',
            status=404,
        )
        yield rsps


def get_calls(mocked):
    return [
        call.request.url
        for call in mocked.calls
        if call.request.method == 'GET'
    ]


class TestTitleAdditions(object):
    def test_new_fields_are_populated(self, facade, mocked):
        title = facade.get_title('tt0111161')

        assert isinstance(title, Title)
        assert title.metacritic == 82
        assert title.spoken_languages == ('en',)
        assert title.countries == ('US',)
        assert title.alternate_titles == ('Il buono',)
        assert title.alternate_titles_count == 1
        assert title.top_rank == {'rank': 1, 'rankType': 'topMovies'}
        assert title.awards_summary == {
            'awardsSummary': {'otherWinsCount': 21}
        }
        assert title.production_status == {'status': 'released'}
        assert title.certificate_reason == (
            'Rated R for language and prison violence'
        )
        assert isinstance(title.trailer, TitleVideo)
        assert title.trailer.url == 'https://video.example/movie.m3u8'
        assert title.trailer.duration_seconds == 131

    def test_existing_fields_unchanged(self, facade, mocked):
        title = facade.get_title('tt0111161')

        assert title.imdb_id == 'tt0111161'
        assert title.title == 'The Shawshank Redemption'
        assert title.year == 1994
        assert title.type == 'movie'
        assert title.rating == 9.3
        assert title.rating_count == 3263412
        assert title.runtime == 142
        assert title.genres == ('drama',)
        assert title.certification == 'R'
        assert title.plot_outline == 'Two imprisoned men bond.'
        assert title.episodes == ()
        assert title.creators[0].imdb_id == 'nm0000175'

    def test_auxiliary_payload_fetched_once(self, facade, mocked):
        facade.get_title('tt0111161')

        template_calls = [
            url
            for url in get_calls(mocked)
            if url.startswith(TITLE_AUXILIARY_URL)
        ]
        assert len(get_calls(mocked)) == 6
        assert len(template_calls) == 1

    def test_cache_ttl_zero_disables_cache(self, tmp_path, mocked):
        client = Imdb(cache_ttl=0)
        client._cachedir = str(tmp_path)
        client.clear_cached_credentials()
        facade = ImdbFacade(client=client)
        facade.get_title('tt0111161')

        assert len(get_calls(mocked)) == 10

    def test_clear_cache(self, facade, mocked):
        facade.get_title('tt0111161')
        facade._client.clear_cache()
        facade.get_title('tt0111161')

        assert len(get_calls(mocked)) == 12


class TestNewTitleMethods(object):
    def test_get_title_watch_options(self, facade, mocked):
        add(
            mocked,
            '/title/tt0111161/watchoptions',
            {
                'optionGroups': [
                    {
                        'displayName': 'STREAMING',
                        'watchOptions': [
                            {
                                'primaryText': 'HBO Max',
                                'secondaryText': 'with subscription',
                                'link': {'uri': 'https://play.max.com/x'},
                                'provider': {'providerId': 'hbo_max'},
                            }
                        ],
                    }
                ]
            },
        )

        options = facade.get_title_watch_options('tt0111161')

        assert len(options) == 1
        assert isinstance(options[0], WatchOption)
        assert options[0].provider == 'HBO Max'
        assert options[0].category == 'streaming'
        assert options[0].url == 'https://play.max.com/x'
        assert options[0].provider_id == 'hbo_max'
        assert options[0].notes == 'with subscription'

    def test_get_title_business(self, facade, mocked):
        add(
            mocked,
            '/title/tt0111161/business',
            {
                'budget': {'amount': 25000000.0, 'currency': 'USD'},
                'gross': {
                    'aggregations': [
                        {
                            'area': 'World-wide',
                            'total': {
                                'amount': 58500000.0,
                                'currency': 'USD',
                            },
                        }
                    ],
                    'regional': [{'region': 'US'}],
                },
                'openingWeekendGross': {'regional': [{'region': 'US'}]},
            },
        )

        business = facade.get_title_business('tt0111161')

        assert isinstance(business, TitleBusiness)
        assert business.budget['amount'] == 25000000.0
        assert business.worldwide_gross == {
            'amount': 58500000.0,
            'currency': 'USD',
        }
        assert business.gross[0]['region'] == 'US'
        assert business.opening_weekend_gross[0]['region'] == 'US'

    def test_get_title_business_without_worldwide_total(self, facade, mocked):
        add(
            mocked,
            '/title/tt0111161/business',
            {
                'gross': {
                    'aggregations': [
                        {'area': 'Domestic', 'total': {'amount': 1.0}}
                    ]
                }
            },
        )

        business = facade.get_title_business('tt0111161')

        assert business.worldwide_gross is None

    def test_get_title_keywords(self, facade, mocked):
        add(
            mocked,
            '/title/tt0111161/keywords',
            {'keywords': ['prison', 'friendship']},
        )

        assert facade.get_title_keywords('tt0111161') == (
            'prison',
            'friendship',
        )

    def test_get_title_certificates(self, facade, mocked):
        add(
            mocked,
            '/title/tt0111161/certificates',
            {
                'certificates': {
                    'CA': [{'certificate': '14A', 'attributes': ['Alberta']}],
                    'US': [{'certificate': 'R'}],
                }
            },
        )

        certificates = facade.get_title_certificates('tt0111161')

        assert len(certificates) == 2
        assert all(isinstance(c, TitleCertificate) for c in certificates)
        assert certificates[0].country == 'CA'
        assert certificates[0].attributes == ('Alberta',)

    def test_get_title_filming_locations(self, facade, mocked):
        add(
            mocked,
            '/title/tt0111161/filminglocations',
            {
                'locations': [
                    {
                        'location': 'Butler, Ohio, USA',
                        'attributes': ['exterior'],
                        'extras': ['The closing scene.'],
                    }
                ]
            },
        )

        locations = facade.get_title_filming_locations('tt0111161')

        assert isinstance(locations[0], FilmingLocation)
        assert locations[0].location == 'Butler, Ohio, USA'
        assert locations[0].notes == ('The closing scene.',)

    def test_get_title_crazy_credits(self, facade, mocked):
        add(
            mocked,
            '/title/tt0111161/crazycredits',
            {'crazycredits': [{'text': 'Credited as "Fat Ass".'}]},
        )

        assert facade.get_title_crazy_credits('tt0111161') == (
            'Credited as "Fat Ass".',
        )

    def test_get_title_principals(self, facade, mocked):
        add(
            mocked,
            '/title/tt0111161/principals',
            {
                'principals': [
                    {
                        'id': '/name/nm0000209/',
                        'name': 'Tim Robbins',
                        'category': 'actor',
                        'job': 'Director',
                        'characters': ['Andy Dufresne'],
                    }
                ]
            },
        )

        principals = facade.get_title_principals('tt0111161')

        assert principals[0].job == 'Director'
        assert isinstance(principals[0], TitleName)
        assert principals[0].imdb_id == 'nm0000209'
        assert principals[0].characters == ('Andy Dufresne',)


class TestNameAdditions(object):
    def test_new_fields_are_populated(self, facade, mocked):
        add(
            mocked,
            '/name/nm0000209/fulldetails',
            name_payload('nm0000209'),
        )
        add(
            mocked,
            '/name/nm0000209/filmography',
            {'filmography': [{'id': '/title/tt0327056/'}]},
        )

        person = facade.get_name('nm0000209')

        assert isinstance(person, Name)
        assert person.jobs == ('actor',)
        assert person.known_for == ('tt0327056',)
        assert person.real_name == 'A Real Name'
        assert person.height_centimeters == 195.58

    @pytest.mark.parametrize(
        'imdb_id,missing',
        [
            ('nm0047113', 'gender'),
            ('nm0087925', 'birthDate'),
            ('nm0374658', 'birthPlace'),
        ],
    )
    def test_missing_optional_fields(self, facade, mocked, imdb_id, missing):
        add(
            mocked,
            '/name/{0}/fulldetails'.format(imdb_id),
            name_payload(imdb_id, missing=(missing,)),
        )
        add(
            mocked,
            '/name/{0}/filmography'.format(imdb_id),
            {'filmography': []},
        )

        person = facade.get_name(imdb_id)

        assert person.name == 'A Person'
        assert person.filmography == ()

    def test_get_name_known_for(self, facade, mocked):
        add(
            mocked,
            '/name/nm0000209/knownfor',
            {
                'knownFor': [
                    {'id': '/title/tt0327056/'},
                    {'id': '/title/tt0105151/'},
                ]
            },
        )

        assert facade.get_name_known_for('nm0000209') == (
            'tt0327056',
            'tt0105151',
        )

    def test_get_name_awards(self, facade, mocked):
        add(
            mocked,
            '/name/nm0000209/awards',
            {
                'awards': [
                    {
                        'awardName': 'Oscar',
                        'category': 'Best Actor',
                        'year': 1995,
                        'isWinner': True,
                        'eventName': 'Academy Awards',
                        'nominations': {
                            'titles': [{'id': '/title/tt0111161/'}]
                        },
                    }
                ]
            },
        )

        awards = facade.get_name_awards('nm0000209')

        assert isinstance(awards[0], Award)
        assert awards[0].name == 'Oscar'
        assert awards[0].won is True
        assert awards[0].title_ids == ('tt0111161',)


class TestClientAdditions(object):
    def test_new_client_methods_return_resource_dicts(self, client, mocked):
        add(
            mocked,
            '/title/tt0111161/keywords',
            {'keywords': ['prison']},
        )

        assert client.get_title_keywords('tt0111161') == {
            'keywords': ['prison']
        }

    def test_cache_ttl_is_a_keyword_argument(self):
        assert Imdb().cache_ttl == 300
        assert Imdb('en_US').locale == 'en_US'
        assert Imdb('en_US', True).exclude_episodes is True
        assert Imdb(cache_ttl=0).cache_ttl == 0

    def test_parse_id_raises_value_error(self, facade):
        with pytest.raises(ValueError):
            facade._parse_id('not an id')

    def test_cached_payload_is_copied(self, client, mocked):
        url = BASE_URI + '/title/tt0111161/keywords'
        add(mocked, '/title/tt0111161/keywords', {'keywords': ['prison']})

        first = client._get_cached(url)
        first['resource']['keywords'].append('mutated')

        assert client._get_cached(url) == {
            'resource': {'keywords': ['prison']}
        }

    def test_cache_is_bounded(self, client, mocked):
        client.CACHE_MAX_ENTRIES = 2
        for index in range(3):
            path = '/title/tt011116{0}/keywords'.format(index)
            add(mocked, path, {'keywords': [str(index)]})
            client._get_cached(BASE_URI + path)

        assert len(client._resource_cache) == 2

    def test_error_payload_is_not_cached(self, client, mocked):
        url = BASE_URI + '/title/tt0111161/keywords'
        mocked.add(responses.GET, url, json={'error': 'transient'})

        assert client._get_cached(url) is None
        assert client._resource_cache == {}
        assert client._get_cached(url) is None
        assert len(get_calls(mocked)) == 2

    def test_unknown_client_attribute_still_raises(self, client):
        with pytest.raises(AttributeError):
            client.get_title_nonexistent
