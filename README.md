# ImdbPie
[![Build Status](https://travis-ci.org/richardasaurus/imdb-pie.png?branch=master)](https://travis-ci.org/richardasaurus/imdb-pie)
[![Downloads](https://pypip.in/d/imdbpie/badge.png)](https://crate.io/packages/imdbpie/)

Python IMDB client using the IMDB json web service made available for their iOS app.

## Installation

To install imdbpie, simply:
```bash
pip install imdbpie
```

## How To Use

### Create an instance of ImdbPie
```python
from imdbpie import Imdb
imdb = Imdb()
imdb = Imdb(anonymize=True) # to proxy requests

# Creating an instance with caching enabled
# Note that the cached responses expire every 2 hours or so.
# The API response itself dictates the expiry time)
imdb = Imdb(cache=True)
# Specify optional cache directory, the default is '/tmp/imdbpiecache'
imdb = Imdb(cache=True, cache_dir='/tmp/imdbpie-cache-here')
```

### Search for a title by its title
```python
>>> imdb.search_for_title("The Dark Knight")
[{'title': "The Dark Knight", 'year':  "2008", 'imdb_id': "tt0468569"},{'title' : "Batman Unmasked", ...}]
```
### Find a title by its imdb_id
```python
>>> title = imdb.get_title_by_id("tt0468569")

>>> title.title
"The Dark Knight"
>>> title.rating
8.1
>>> title.certification
"PG-13"
```
### Find a person by their imdb_id
```python
person = imdb.get_person_by_id("nm0000151")

>>> person.name
"Morgan Freeman"
>>> person.imdb_id
"nm0000151"
```

### Find a title trailer poster
```python
title = imdb.get_title_by_id("tt1210166")
>>> title.trailer_image_urls
["http://ia.media-imdb.com/images/M/MV5BODM1NDMxMTI3M15BMl5BanBnXkFtZTcwMDAzODY1Ng@@._V1_.jpg",...]
```

### Find the top 250 movies ever
```python
>>> imdb.top_250()
[{'title': 'The Shawshank Redemption', 'year': '1994', 'type': 'feature', 'rating': 9.3,...}, ...]
```

### Get the current popular shows
```python
>>> imdb.popular_shows()
[{'title': 'Glee', 'year': "2009", 'imdb_id': 'tt1327801'}, {'title': "Dexter", ...}]
```
### Check if a movie exists, by imdb id
Returns either True or False
```python
>>> imdb.title_exists('tt1327801')
True
```

### Get images for a person
Returns a list of image objects with the following attributes (caption, url, width, height)
```python
>>> imdb.get_person_images("nm0000033")
[<Image: u'Alfred Hitchcock'>, <Image: u'"Psycho" Dir. Alfred Hitchcock 1960 Paramount'>,...]
```
### Get images for a title
Returns a list of image objects with the following attributes (caption, url, width, height)
```python
>>> imdb.get_title_images("tt0468569")
[<Image: u'Morgan Freeman and Frank Darabont in The Shawshank Redemption'>,...]
```
### Get reviews for a title
Returns a list of Review objects with the following attributes (username, text, date, rating, summary, status, user_location, user_score, user_score_count)
```python
>>> imdb.get_title_reviews("tt0468569")
[<Review: u'Why do I want to wri'>, <Review: u'Can Hollywood, usua'>,...]
```

### Example: Get a title's credit information and check categorisation
```python
title = imdb.get_title_by_id("tt1210166")
for person in title.credits:
    # check if they are a writer
    if person.token == 'writers':
        print(person.name + ' is a writer')
    else:
        print(person.name + ' is not a writer')
```

## Requirements

    1. Python 2 or 3
    2. See requirements.txt

## Running the tests

```bash
pip install -r test_requirements.txt
py.test src/tests
```


