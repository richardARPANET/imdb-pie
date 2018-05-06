from collections.abc import Sequence
from datetime import date

from dataclasses import dataclass


@dataclass
class Image:
    url: str
    width: int
    height: int


class TitleEpisodes(Sequence):

    def __init__(self, facade, imdb_id):
        self._facade = facade
        episodes = self._facade._client.get_title_episodes(
            imdb_id=imdb_id
        )
        self._episode_imdb_ids = []
        for season in episodes['seasons']:
            for episode in season['episodes']:
                imdb_id = self._facade._parse_id(episode['id'])
                self._episode_imdb_ids.append(imdb_id)
        self._count = len(self._episode_imdb_ids)

    def __len__(self):
        return self._count

    def __bool__(self):
        return self._count > 0

    def __getitem__(self, index):
        imdb_id = self._episode_imdb_ids[index]
        return self._facade.get_title_episode(imdb_id=imdb_id)


@dataclass
class Title:
    imdb_id: str
    title: str
    type: str
    certification: str
    year: int
    genres: tuple
    writers: tuple
    creators: tuple
    credits: tuple
    directors: tuple
    stars: tuple
    image: Image
    episodes: TitleEpisodes
    rating_count: int = 0
    rating: float = None
    plot_outline: str = None
    release_date: date = None
    releases: tuple = ()

    def __repr__(self):
        return 'Title(imdb_id={0}, title={1})'.format(self.imdb_id, self.title)


@dataclass
class TitleEpisode:
    imdb_id: str
    title: str
    type: str
    season: int
    episode: int
    certification: str
    year: int
    genres: tuple
    writers: tuple
    creators: tuple
    credits: tuple
    directors: tuple
    stars: tuple
    image: Image
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
    category: str
    imdb_id: str
    job: str = None
    characters: tuple = ()


@dataclass
class Name:
    name: str
    imdb_id: str
    image: Image
    birth_place: str
    gender: str
    bios: tuple
    date_of_birth: date
    filmography: tuple
