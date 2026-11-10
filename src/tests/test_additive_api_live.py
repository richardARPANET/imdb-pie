# coding: utf-8
from __future__ import absolute_import, unicode_literals

import pytest

from imdbpie import ImdbFacade
from imdbpie.objects import (
    Award,
    FilmingLocation,
    TitleBusiness,
    TitleCertificate,
    TitleName,
    TitleVideo,
    WatchOption,
)

pytestmark = pytest.mark.live

TITLE_ID = 'tt0111161'  # The Shawshank Redemption
SERIES_ID = 'tt0903747'  # Breaking Bad
NAME_ID = 'nm0000209'  # Tim Robbins


@pytest.fixture(scope='module')
def facade():
    return ImdbFacade()


def test_title_new_fields(facade):
    title = facade.get_title(TITLE_ID)

    assert isinstance(title.metacritic, int)
    assert title.metacritic > 0
    assert 'en' in title.spoken_languages
    assert 'US' in title.countries
    assert len(title.alternate_titles) > 0
    assert title.alternate_titles_count > 0
    assert isinstance(title.top_rank, dict)
    assert title.top_rank['rank'] > 0
    assert isinstance(title.trailer, TitleVideo)
    assert title.trailer.url
    assert title.certificate_reason
    assert title.production_status


def test_series_has_episodes_and_rank(facade):
    series = facade.get_title(SERIES_ID)

    assert series.type == 'tvseries'
    assert len(series.episodes) > 0
    assert series.spoken_languages


def test_watch_options(facade):
    options = facade.get_title_watch_options(TITLE_ID)

    assert len(options) > 0
    assert all(isinstance(option, WatchOption) for option in options)
    assert all(option.provider for option in options)
    assert {'streaming', 'rent/buy'} <= {o.category for o in options}


def test_business(facade):
    business = facade.get_title_business(TITLE_ID)

    assert isinstance(business, TitleBusiness)
    assert business.budget['currency'] == 'USD'
    assert business.budget['amount'] > 0
    assert business.worldwide_gross['amount'] > 0


def test_keywords(facade):
    keywords = facade.get_title_keywords(TITLE_ID)

    assert len(keywords) > 0
    assert all(isinstance(keyword, str) for keyword in keywords)


def test_certificates(facade):
    certificates = facade.get_title_certificates(TITLE_ID)

    assert len(certificates) > 0
    assert all(
        isinstance(certificate, TitleCertificate)
        for certificate in certificates
    )
    assert any(certificate.country == 'US' for certificate in certificates)


def test_filming_locations(facade):
    locations = facade.get_title_filming_locations(TITLE_ID)

    assert len(locations) > 0
    assert all(isinstance(location, FilmingLocation) for location in locations)
    assert all(location.location for location in locations)


def test_crazy_credits(facade):
    crazy_credits = facade.get_title_crazy_credits(TITLE_ID)

    assert len(crazy_credits) > 0
    assert all(isinstance(credit, str) for credit in crazy_credits)


def test_principals(facade):
    principals = facade.get_title_principals(TITLE_ID)

    assert len(principals) > 0
    assert all(isinstance(principal, TitleName) for principal in principals)
    assert principals[0].imdb_id.startswith('nm')
    assert any(principal.characters for principal in principals)


def test_name_new_fields(facade):
    person = facade.get_name(NAME_ID)

    assert len(person.jobs) > 0
    assert len(person.known_for) > 0
    assert all(imdb_id.startswith('tt') for imdb_id in person.known_for)
    assert person.real_name
    assert person.height_centimeters > 0


def test_name_known_for(facade):
    known_for = facade.get_name_known_for(NAME_ID)

    assert len(known_for) > 0
    assert all(imdb_id.startswith('tt') for imdb_id in known_for)


def test_name_awards(facade):
    awards = facade.get_name_awards(NAME_ID)

    assert len(awards) > 0
    assert all(isinstance(award, Award) for award in awards)
    assert all(award.name for award in awards)


@pytest.mark.parametrize(
    'imdb_id',
    ['nm0047113', 'nm0374658'],
)
def test_name_without_optional_fields(facade, imdb_id):
    """These used to raise KeyError from the facade."""
    person = facade.get_name(imdb_id)

    assert person.name
    assert person.filmography is not None
