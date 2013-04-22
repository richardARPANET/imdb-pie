from imdbpie import Imdb

imdb = Imdb({'anonymize': False,
             'locale': 'en_US',
             'exclude_episodes': False})


def run_tests():
    print(movie.title)
    print('year', movie.year)
    print('type', movie.type)
    print('tagline', movie.tagline)
    print('rating', movie.rating)
    print('certification', movie.certification)
    print('genres', movie.genres)
    print('plot', movie.plot)
    print('runtime', movie.runtime)
    print('writers', movie.writers)
    print('directors', movie.directors)
    print('creators', movie.creators)
    print('cast summary', movie.cast_summary)
    print('full credits', movie.credits)

if __name__ == '__main__':
    movie = imdb.find_movie_by_id('tt0705926')
    run_tests()
