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
imdb = Imdb()
imdb = Imdb({'anonymize' : True}) # to proxy requests

# Creating an instance with caching enabled
# Note that the cached responses expire every 2 hours or so.
# The API response itself dictates the expiry time)
imdb = Imdb({'cache': True})
# Specify optional cache directory, the default is '/tmp/imdbpiecache'
imdb = Imdb({'cache': True, 'cache_dir': '/tmp/imdbpie-cache-here'})
```

### Search for a movie by title
```python
imdb.find_by_title("The Dark Knight") => [{'title' : "The Dark Knight", 'year' :  "2008", 'imdb_id' : "tt0468569"}, {'title' : "Batman Unmasked", ...}]
```
### Find a movie by its imdb_id
```python
movie = imdb.find_movie_by_id("tt0468569")

movie.title => "The Dark Knight"
movie.rating => 8.1
movie.certification => "PG-13"
```

### Find a movie trailer poster
```python
movie = imdb.find_movie_by_id("tt1210166")
movie.trailer_url => "http://ia.media-imdb.com/images/M/MV5BODM1NDMxMTI3M15BMl5BanBnXkFtZTcwMDAzODY1Ng@@._V1_.jpg"
```

### Find the top 250 movies ever
```python
imdb.top_250() => [{'title': 'The Shawshank Redemption', 'year': '1994', 'type': 'feature', 'rating': 9.3,...}, ...]
```

### Get the current popular shows
```python
imdb.popular_shows() => [{'title' : "Glee", 'year' : "2009", 'imdb_id' => "tt1327801"}, {'title' : "Dexter", ...}]
```
### Check if a movie exists, by imdb id
Returns either True or False
```python
imdb.movie_exists('tt1327801') => True
```

### Check an imdb id is of valid format (tt0000000), and try to fix if not
```python
imdb.validate_id('tt1000') => tt0001000
```
### Get images for a person
Returns a list of image objects with the following attributes (caption, url, width, height)
```python
images = imdb.person_images("tt0468569")
```
### Get images for a movie or show
Returns a list of image objects with the following attributes (caption, url, width, height)
```python
images = imdb.title_images("tt0468569")
```

### Get a title's credit information and check categorisation
```python
movie = imdb.find_movie_by_id("tt1210166")
for person in movie.credits:
    # check if they are a writer
    if person.token == 'writers':
        print person.name + ' is a writer'
    else:
        print person.name + ' is not a writer'
```

## Requirements

    1. Python 2 or 3
    2. Python requests - python-requests.org

## Running the tests

Run:

```bash
nosetests
```


