import re
from datetime import date

from dateutil.parser import parse
from dataclasses import dataclass

REGEX_IMDB_ID = re.compile(r'([a-zA-Z]{2}[0-9]{7})')

@dataclass
class Title:
    title: str
    type: str
    year: int
    genres: tuple
    writers: tuple
    creators: tuple
    credits: tuple
    directors: tuple
    rating_count: int = 0
    rating: float = None
    plot_outline: str = None
    release_date: date = None
    releases: tuple = ()


@dataclass
class TitleRelease:
    date: date
    region: str


@dataclass
class TitleName:
    name: str
    job: str
    category: str
    imdb_id: str


class ImdbFacade(object):

    def __init__(self, client):
        self._client = client

    def get_title(self, imdb_id):
        base_title_data = self._client.get_title(imdb_id=imdb_id)
        title = base_title_data['base']['title']
        year = base_title_data['base']['year']
        rating = float(base_title_data['ratings']['rating'])
        type_ = base_title_data['base']['titleType']
        releases_data = self._client.get_title_releases(imdb_id=imdb_id)
        release_date = parse(releases_data['releases'][0]['date']).date()
        releases = tuple(
            TitleRelease(date=parse(r['date']).date(), region=r['region'])
            for r in  releases_data['releases']
        )
        rating_count = base_title_data['ratings']['ratingCount']
        plot_outline = base_title_data['plot']['outline']['text']

        top_crew_data = self._client.get_title_top_crew(imdb_id=imdb_id)
        writers = self._get_writers(top_crew_data)
        directors = self._get_directors(top_crew_data)
        creators = self._get_creators(top_crew_data)
        genres = tuple(
            g.lower() for g in
            self._client.get_title_genres(imdb_id=imdb_id)['genres']
        )
        credits_data = self._client.get_title_credits(imdb_id=imdb_id)
        credits = self._get_credits(credits_data)
        return Title(
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
        )

    def _get_writers(self, top_crew_data):
        return tuple(
            TitleName(
                name=i['name'],
                job=i.get('job'),
                category=i.get('category'),
                imdb_id=REGEX_IMDB_ID.findall(i['id'])[0]
            ) for i in top_crew_data['writers']
        )

    def _get_creators(self, top_crew_data):
        return tuple(
            TitleName(
                name=i['name'],
                job=i.get('job'),
                category=i.get('category'),
                imdb_id=REGEX_IMDB_ID.findall(i['id'])[0]
            ) for i in top_crew_data['writers']
            if i.get('job') == 'creator'
        )

    def _get_directors(self, top_crew_data):
        return tuple(
            TitleName(
                name=i['name'],
                job=i.get('job'),
                category=i.get('category'),
                imdb_id=REGEX_IMDB_ID.findall(i['id'])[0]
            ) for i in top_crew_data['directors']
        )

    def _get_credits(self, credits_data):
        credits = []
        for category in credits_data['credits']:
            for item in credits_data['credits'][category]:
                credits.append(TitleName(
                    name=item['name'],
                    category=item.get('category'),
                    job=item.get('job'),
                    imdb_id=REGEX_IMDB_ID.findall(item['id'])[0]
                ))
        return tuple(credits)
