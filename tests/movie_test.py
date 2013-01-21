from imdbpie import Imdb
import re

imdb = Imdb({'anonymize' : False})
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
    if movie.plot == "Remy is a young rat in the French countryside who arrives in Paris, only to find out that his cooking idol is dead. When he makes an unusual alliance with a restaurant's new garbage boy, the culinary and personal adventures begin despite Remy's family's skepticism and the rat-hating world of humans.":
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
