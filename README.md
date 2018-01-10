# ImdbPie

[![PyPI](https://img.shields.io/pypi/v/imdbpie.svg)](https://pypi.python.org/pypi/imdb-pie)
[![Python Versions](https://img.shields.io/pypi/pyversions/imdbpie.svg)](https://pypi.python.org/pypi/imdb-pie)
[![Build Status](https://travis-ci.org/richardasaurus/imdb-pie.png?branch=master)](https://travis-ci.org/richardasaurus/imdb-pie)

Python IMDB client using the IMDB json web service made available for their iOS app.

## Installation

To install imdbpie, simply:
```bash
pip install imdbpie
```

## How To Use

### Initialise the client
```python
from imdbpie import Imdb
imdb = Imdb()
```

### Available methods

NOTE: For each client method, if the resource cannot be found they will raise `LookupError`, if there is an API error then `ImdbAPIError` will raise.

#### get_title

```python
imdb.get_title('tt0111161')
# Returns a dict containing title information
```

#### get_title_genres

```python
imdb.get_title_genres('tt0303461')
# Returns a dict containing genres information
```

#### get_title_episodes

```python
imdb.get_title_episodes('tt0303461')
# Returns a dict containing season and episodes information
```

#### get_title_plot

```python
imdb.get_title_plot('tt0111161')
# Returns a dict containing plot information
```

#### get_title_user_reviews

```python
imdb.get_title_user_reviews('tt0111161')
# Returns a dict containing user review information
```

#### get_title_metacritic_reviews

```python
imdb.get_title_metacritic_reviews('tt0111161')
# Returns a dict containing metacritic review information
```

#### get_title_images

```python
imdb.get_title_images('tt0111161')
# Returns a dict containing title images information
```

#### title_exists

```python
imdb.title_exists('tt0111161')
# Returns True if exists otherwise False
```

#### search_for_title
```python
imdb.search_for_title("The Dark Knight")
# Returns list of dict results
[{'title': "The Dark Knight", 'year':  "2008", 'imdb_id': "tt0468569"},{'title' : "Batman Unmasked", ...}]
```

#### search_for_name
```python
imdb.search_for_name("Christian Bale")
# Returns list of dict results
[{'imdb_id': 'nm0000288', 'name': 'Christian Bale'},{'imdb_id': 'nm7635250', ...}]
```

#### get_name

```python
imdb.get_name('nm0000151')
# Returns a dict containing person/name information
```

#### get_name_images

```python
imdb.get_name_images('nm0000032')
# Returns a dict containing person/name images information
```

#### validate_imdb_id

```python
imdb.validate_imdb_id('tt0111161')
# Raises `ValueError` if not valid
```

#### get_popular_titles

```python
imdb.get_popular_titles()
# Returns a dict containing popular titles information
```

#### get_popular_shows

```python
imdb.get_popular_shows()
# Returns a dict containing popular titles information
```

#### get_popular_movies

```python
imdb.get_popular_movies()
# Returns a dict containing popular titles information
```

## Requirements

    1. Python 2 or 3
    2. See requirements.txt

## Running the tests

```bash
pip install -r test_requirements.txt
py.test src/tests
```


