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
    print('writers summary', movie.writers_summary)
    print('creators', movie.creators)
    print('cast summary', movie.cast_summary)
    print('full cast', movie.cast)

if __name__ == '__main__':
    movie = imdb.find_movie_by_id('tt0111161')
    run_tests()
