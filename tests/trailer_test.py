from imdbpie import Imdb
import re

imdb = Imdb({'anonymize' : False})
movie = imdb.find_movie_by_id("tt1210166")

def run_tests():
    print('have a trailer_url:')
    match = re.findall(r'http://ia.media-imdb.com/images/.*/', movie.trailer_url)[0]
    if match:
        print('passed')



if __name__ == '__main__':
    run_tests()
