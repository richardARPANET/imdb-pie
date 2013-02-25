# ImdbPie

Python IMDB client using the IMDB json web service made available for their iOS app.

## How To Use

### Create an instance of ImdbPie

    imdb = Imdb()
    imdb = Imdb({'anonymize' : True}) # to proxy requests

### Search for a movie by title

    imdb.find_by_title("The Dark Knight") => [{'title' : "The Dark Knight", 'year' :  "2008", 'imdb_id' : "tt0468569"}, {'title' : "Batman Unmasked", ...}]

### Find a movie by its imdb_id

    movie = imdb.find_movie_by_id("tt0468569")

    movie.title => "The Dark Knight"
    movie.rating => 8.1
    movie.certification => "PG-13"

### Find a movie trailer poster

    movie = imdb.find_movie_by_id("tt1210166")
    movie.trailer_url => "http://ia.media-imdb.com/images/M/MV5BODM1NDMxMTI3M15BMl5BanBnXkFtZTcwMDAzODY1Ng@@._V1_.jpg"

### Find the top 250 movies ever

    imdb.top_250() => [{'title': 'The Shawshank Redemption', 'year': '1994', 'type': 'feature', 'rating': 9.3,...}, ...]


### Get the current popular shows

    imdb.popular_shows() => [{'title' : "Glee", 'year' : "2009", 'imdb_id' => "tt1327801"}, {'title' : "Dexter", ...}]

### Check if a movie exists, by imdb id

    imdb.movie_exists('tt1327801') => True

### Check an imdb id is of valid format (tt0000000), and try to fix if not

    imdb.validate_id('tt1000') => tt0001000

## Requirements

    1. Python3.3
    2. Python requests - python-requests.org

## Tests

    Test .py files can be found in /tests, run these to ensure ImdbPie is working 100%.


