# ImdbPie
[![Build Status](https://travis-ci.org/richardasaurus/imdb-pie.png?branch=master)](https://travis-ci.org/richardasaurus/imdb-pie)

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
```

### Search for a title by its title
```python
>>> imdb.search_for_title("The Dark Knight")
[{'title': "The Dark Knight", 'year':  "2008", 'imdb_id': "tt0468569"},{'title' : "Batman Unmasked", ...}]
```
### Search for person by their name
```python
>>> imdb.search_for_person("Christian Bale")
[{'imdb_id': 'nm0000288', 'name': 'Christian Bale'},{'imdb_id': 'nm7635250', ...}]
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
>>> person = imdb.get_person_by_id("nm0000151")
>>> person.name
"Morgan Freeman"
>>> person.imdb_id
"nm0000151"
>>> person.photo_url
"https://images-na.ssl-images-amazon.com/images/M/MV5BNzkwNTY1MDYxOF5BMl5BanBnXkFtZTgwNjk4NjM3OTE@._V1_.jpg"
```

### Find all episodes for a title by its imdb_id

```python
>>> imdb.get_episodes('tt0096697')
[<Episode: u'Simpsons Roasting on an Open Fire' - u'tt0348034'>,
 <Episode: u'Bart the Genius' - u'tt0756593'>,
 <Episode: u"Homer's Odyssey" - u'tt0701124'>,...]

>>> episode.release_date
'1989-12-17'
>>> episode.title
'Simpsons Roasting on an Open Fire'
>>> episode.series_name
'The Simpsons'
>>> episode.type
'tv_episode'
>>> episode.year
1989
>>> episode.season
1
>>> episode.episode
1
>>> episode.imdb_id
'tt0348034'
```

### Find a title trailer poster
```python
>>> title = imdb.get_title_by_id("tt1210166")
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
[{
	'image': {
		'height': 2048,
		'url': 'https://images-na.ssl-images-amazon.com/images/M/MV5BMjE3NTQ1NDg1Ml5BMl5BanBnXkFtZTgwNzY2NDA0MjI@._V1_.jpg',
		'width': 1382
	},
	'principals': [{
			'name': 'Emilia Clarke',
			'nconst': 'nm3592338'
		},
        ...
	],
	'tconst': 'tt0944947',
	'title': 'Game of Thrones',
	'type': 'tv_series',
	'year': '2011'
}]
```

### Get the current popular movies
```python
>>> imdb.popular_movies()
[{
	'prev': 1,
	'object': {
		'tconst': 'tt0944947',
		'title': 'Game of Thrones',
		'image': {
			'url': 'https://images-na.ssl-images-amazon.com/images/M/MV5BMjE3NTQ1NDg1Ml5BMl5BanBnXkFtZTgwNzY2NDA0MjI@._V1_.jpg',
			'width': 1382,
			'height': 2048
		},
		'year': '2011',
		'principals': [{
			'nconst': 'nm3592338',
			'name': 'Emilia Clarke'
		},
		...
        ],
		'type': 'tv_series'
	},
	'rank': 1
}]
```

### Check if a title exists
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
>>> imdb.get_title_reviews("tt0468569", max_results=15)
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


