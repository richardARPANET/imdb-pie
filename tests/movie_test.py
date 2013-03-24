import re

from imdbpie import Imdb


imdb = Imdb({'anonymize': False})
movie = imdb.find_movie_by_id("tt0382932")


def run_tests():
    print('have a title:')
    if movie.title == 'Ratatouille':
        print('passed')

    print('have an imdb id:')
    if movie.imdb_id == 'tt0382932':
        print('passed')

    print('have a tagline:')
    if movie.tagline == 'Dinner is served... Summer 2007':
        print('passed')

    print('have a plot:')
    if movie.plot == "With dreams of becoming a chef, a culinary genius in" \
                     " the form of a rat, makes an unusual alliance with a young kitchen worker at a famed restaurant.":
        print('passed')

    print('have a runtime:')
    if movie.runtime == '111 min':
        print('passed')

    print('have a rating:')
    if movie.rating == 8:
        print('passed')

    print('have a poster url:')
    match = re.findall(r'http://ia.media-imdb.com/images/.*/', movie.poster_url)[0]
    if match:
        print('passed')

    print('have a release date:')
    if movie.release_date == '2007-06-29':
        print('passed')

    print('have a certification')
    if movie.certification == 'G':
        print('passed')

    print('have trailers:')
    if movie.trailers is not None:
        print('passed')

    print('have genres:')
    if movie.genres is not None:
        print('passed')

    print('have directors:')
    if movie.directors is not None:
        print('passed')

    print('have writers:')
    if movie.writers is not None:
        print('passed')

    print('have a title:')
    if movie.title == 'Ratatouille':
        print('passed')

if __name__ == '__main__':
    run_tests()
