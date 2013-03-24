from imdbpie import Imdb

imdb = Imdb({'anonymize': False})


def run_tests():
    print(movie.title)
    print('year', movie.year)
    print('type', movie.type)
    print('tagline', movie.tagline)
    print('rating', movie.rating)
    print('genres', movie.genres)
    print('plot', movie.plot)
    print('runtime', movie.runtime)
    print('writers', movie.writers)
    print('creators', movie.creators)
    print('actors', movie.actors)

if __name__ == '__main__':
    movie = imdb.find_movie_by_id('tt0000764')
    run_tests()
