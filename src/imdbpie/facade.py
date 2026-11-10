# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from dateutil.parser import parse

from .imdbpie import Imdb
from .objects import (
    Award,
    FilmingLocation,
    Image,
    Name,
    NameSearchResult,
    Title,
    TitleBusiness,
    TitleCertificate,
    TitleEpisodes,
    TitleName,
    TitleRelease,
    TitleSearchResult,
    TitleVideo,
    WatchOption,
)

REGEX_IMDB_ID = re.compile(r'([a-zA-Z]{2}[0-9]{7,8})')


class ImdbFacade(object):
    def __init__(self, client=None):
        self._client = client or Imdb()

    def get_title(self, imdb_id):
        title_data, title_aux_data = self._get_title_data(imdb_id=imdb_id)
        try:
            runtime = title_aux_data['runningTimes'][0]['timeMinutes']
        except (KeyError, IndexError):
            runtime = None
        try:
            episodes = TitleEpisodes(facade=self, imdb_id=imdb_id)
        except LookupError:
            episodes = ()
        try:
            season = title_aux_data['season']
            episode = title_aux_data['episode']
        except KeyError:
            season = None
            episode = None
        return Title(
            season=season,
            episode=episode,
            episodes=episodes,
            runtime=runtime,
            **title_data
        )

    def get_name(self, imdb_id):
        name_data = self._client.get_name(imdb_id=imdb_id)
        base = name_data['base']
        name = base['name']
        imdb_id = self._parse_id(base['id'])

        try:
            image_data = base['image']
            image = Image(
                url=image_data['url'],
                height=image_data['height'],
                width=image_data['width'],
            )
        except KeyError:
            image = None

        gender = (base.get('gender') or '').lower() or None
        birth_date = base.get('birthDate')
        date_of_birth = parse(birth_date).date() if birth_date else None
        birth_place = base.get('birthPlace')
        try:
            bios = tuple(b['text'] for b in base['miniBios'])
        except KeyError:
            bios = ()

        filmography_data = self._client.get_name_filmography(imdb_id)
        filmography = tuple(
            self._parse_id(f['id']) for f in filmography_data['filmography']
        )
        known_for = tuple(
            self._parse_id(item['id'])
            for item in (name_data.get('knownFor') or ())
            if item.get('id')
        )
        return Name(
            name=name,
            imdb_id=imdb_id,
            date_of_birth=date_of_birth,
            gender=gender,
            birth_place=birth_place,
            bios=bios,
            image=image,
            filmography=filmography,
            jobs=tuple(name_data.get('jobs') or ()),
            known_for=known_for,
            real_name=base.get('realName'),
            height_centimeters=base.get('heightCentimeters'),
        )

    def search_for_name(self, query):
        results = []
        for result in self._client.search_for_name(query):
            result = NameSearchResult(
                imdb_id=result['imdb_id'],
                name=result['name'],
            )
            results.append(result)
        return tuple(results)

    def search_for_title(self, query):
        results = []
        for result in self._client.search_for_title(query):
            if result['year']:
                year = int(result['year'])
            else:
                year = None
            result = TitleSearchResult(
                imdb_id=result['imdb_id'],
                title=result['title'],
                type=result['type'],
                year=year,
            )
            results.append(result)
        return tuple(results)

    def _get_writers(self, top_crew_data):
        return tuple(
            TitleName(
                name=i['name'],
                job=i.get('job'),
                category=i.get('category'),
                imdb_id=self._parse_id(i['id']),
            )
            for i in top_crew_data['writers']
        )

    def _get_stars(self, principals_data):
        return tuple(
            TitleName(
                name=i['name'],
                job=i.get('job'),
                characters=tuple(i.get('characters', ())),
                category=i.get('category'),
                imdb_id=self._parse_id(i['id']),
            )
            for i in principals_data
        )

    def _get_creators(self, top_crew_data):
        return tuple(
            TitleName(
                name=i['name'],
                job=i.get('job'),
                category=i.get('category'),
                imdb_id=self._parse_id(i['id']),
            )
            for i in top_crew_data['writers']
            if i.get('job') == 'creator'
        )

    def _get_directors(self, top_crew_data):
        return tuple(
            TitleName(
                name=i['name'],
                job=i.get('job'),
                category=i.get('category'),
                imdb_id=self._parse_id(i['id']),
            )
            for i in top_crew_data['directors']
        )

    def _get_credits(self, credits_data):
        credits = []
        for category in credits_data.get('credits', ()):
            for item in credits_data['credits'][category]:
                credits.append(
                    TitleName(
                        name=item['name'],
                        category=item.get('category'),
                        job=item.get('job'),
                        imdb_id=self._parse_id(item['id']),
                    )
                )
        return tuple(credits)

    def _parse_id(self, string):
        match = REGEX_IMDB_ID.search(string or '')
        if not match:
            raise ValueError('invalid imdb id: {0!r}'.format(string))
        return match.group(1)

    def _get_title_data(self, imdb_id):
        base_title_data = self._client.get_title(imdb_id=imdb_id)
        top_crew_data = self._client.get_title_top_crew(imdb_id=imdb_id)
        title_aux_data = self._client.get_title_auxiliary(imdb_id=imdb_id)
        credits_data = self._client.get_title_credits(imdb_id=imdb_id)

        title = base_title_data['base']['title']
        year = base_title_data['base'].get('year')
        try:
            rating = float(base_title_data['ratings']['rating'])
        except KeyError:
            rating = None
        type_ = base_title_data['base']['titleType'].lower()

        try:
            releases_data = self._client.get_title_releases(imdb_id=imdb_id)
        except LookupError:
            release_date = None
            releases = ()
        else:
            release_date = parse(releases_data['releases'][0]['date']).date()
            releases = tuple(
                TitleRelease(date=parse(r['date']).date(), region=r['region'])
                for r in releases_data['releases']
            )

        try:
            rating_count = base_title_data['ratings']['ratingCount']
        except KeyError:
            rating_count = 0

        try:
            plot_outline = base_title_data['plot']['outline']['text']
        except KeyError:
            plot_outline = None

        writers = self._get_writers(top_crew_data)
        directors = self._get_directors(top_crew_data)
        creators = self._get_creators(top_crew_data)
        try:
            genres = tuple(g.lower() for g in title_aux_data.get('genres'))
        except TypeError:
            genres = ()
        credits = self._get_credits(credits_data)

        try:
            certification = title_aux_data['certificate']['certificate']
        except (KeyError, TypeError):
            certification = None
        stars = self._get_stars(title_aux_data['principals'])
        try:
            image_data = title_aux_data['image']
            image = Image(
                url=image_data['url'],
                height=image_data['height'],
                width=image_data['width'],
            )
        except KeyError:
            image = None
        metacritic_info = title_aux_data.get('metacriticInfo') or {}
        certificate_data = title_aux_data.get('certificate') or {}
        return (
            dict(
                imdb_id=imdb_id,
                title=title,
                year=year,
                rating=rating,
                type=type_,
                release_date=release_date,
                releases=releases,
                plot_outline=plot_outline,
                rating_count=rating_count,
                writers=writers,
                directors=directors,
                creators=creators,
                genres=genres,
                credits=credits,
                certification=certification,
                image=image,
                stars=stars,
                metacritic=metacritic_info.get('metaScore'),
                awards_summary=title_aux_data.get('awards'),
                spoken_languages=tuple(
                    title_aux_data.get('spokenLanguages') or ()
                ),
                countries=tuple(title_aux_data.get('origins') or ()),
                alternate_titles=tuple(
                    title_aux_data.get('alternateTitlesSample') or ()
                ),
                alternate_titles_count=(
                    title_aux_data.get('alternateTitlesCount') or 0
                ),
                top_rank=title_aux_data.get('topRank'),
                trailer=self._parse_trailer(title_aux_data.get('videos')),
                production_status=title_aux_data.get('productionStatus'),
                certificate_reason=certificate_data.get('ratingReason'),
            ),
            title_aux_data,
        )

    @staticmethod
    def _parse_trailer(videos_data):
        trailer = (videos_data or {}).get('mainTrailer')
        if not trailer:
            return None
        url = None
        for encoding in trailer.get('encodings') or ():
            if encoding.get('play'):
                url = encoding['play']
                break
        return TitleVideo(
            content_type=trailer.get('contentType'),
            description=trailer.get('description'),
            url=url,
            duration_seconds=trailer.get('durationSeconds'),
        )

    def get_title_watch_options(self, imdb_id):
        data = self._client.get_title_watch_options(imdb_id=imdb_id)
        options = []
        for group in data.get('optionGroups') or ():
            category = (group.get('displayName') or '').lower()
            for option in group.get('watchOptions') or ():
                link = option.get('link') or {}
                provider = option.get('provider') or {}
                options.append(
                    WatchOption(
                        provider=option.get('primaryText'),
                        category=category,
                        url=link.get('uri'),
                        provider_id=provider.get('providerId'),
                        notes=option.get('secondaryText'),
                    )
                )
        return tuple(options)

    def get_title_business(self, imdb_id):
        data = self._client.get_title_business(imdb_id=imdb_id)
        gross = data.get('gross') or {}
        aggregations = gross.get('aggregations') or []
        worldwide_gross = None
        for aggregation in aggregations:
            if aggregation.get('area') == 'World-wide':
                worldwide_gross = aggregation.get('total')
                break
        opening_weekend = data.get('openingWeekendGross') or {}
        return TitleBusiness(
            budget=data.get('budget'),
            worldwide_gross=worldwide_gross,
            gross=tuple(gross.get('regional') or ()),
            opening_weekend_gross=tuple(opening_weekend.get('regional') or ()),
        )

    def get_title_keywords(self, imdb_id):
        data = self._client.get_title_keywords(imdb_id=imdb_id)
        return tuple(data.get('keywords') or ())

    def get_title_certificates(self, imdb_id):
        data = self._client.get_title_certificates(imdb_id=imdb_id)
        certificates = []
        for country, entries in (data.get('certificates') or {}).items():
            for entry in entries or ():
                certificates.append(
                    TitleCertificate(
                        country=country,
                        certificate=entry.get('certificate'),
                        attributes=tuple(entry.get('attributes') or ()),
                    )
                )
        return tuple(certificates)

    def get_title_filming_locations(self, imdb_id):
        data = self._client.get_title_filming_locations(imdb_id=imdb_id)
        return tuple(
            FilmingLocation(
                location=item.get('location'),
                attributes=tuple(item.get('attributes') or ()),
                notes=tuple(item.get('extras') or ()),
            )
            for item in (data.get('locations') or ())
        )

    def get_title_crazy_credits(self, imdb_id):
        data = self._client.get_title_crazy_credits(imdb_id=imdb_id)
        return tuple(
            item['text']
            for item in (data.get('crazycredits') or ())
            if item.get('text')
        )

    def get_title_principals(self, imdb_id):
        data = self._client.get_title_principals(imdb_id=imdb_id)
        return tuple(
            TitleName(
                name=item.get('name'),
                category=item.get('category'),
                imdb_id=(
                    self._parse_id(item['id']) if item.get('id') else None
                ),
                job=item.get('job'),
                characters=tuple(item.get('characters') or ()),
            )
            for item in (data.get('principals') or ())
        )

    def get_name_known_for(self, imdb_id):
        data = self._client.get_name_known_for(imdb_id=imdb_id)
        return tuple(
            self._parse_id(item['id'])
            for item in (data.get('knownFor') or ())
            if item.get('id')
        )

    def get_name_awards(self, imdb_id):
        data = self._client.get_name_awards(imdb_id=imdb_id)
        awards = []
        for item in data.get('awards') or ():
            titles = (item.get('nominations') or {}).get('titles') or ()
            awards.append(
                Award(
                    name=item.get('awardName'),
                    category=item.get('category'),
                    year=item.get('year'),
                    won=bool(item.get('isWinner')),
                    event_name=item.get('eventName'),
                    title_ids=tuple(
                        self._parse_id(title['id'])
                        for title in titles
                        if title.get('id')
                    ),
                )
            )
        return tuple(awards)
