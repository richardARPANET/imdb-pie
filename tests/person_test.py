from imdbpie import Imdb

imdb = Imdb({'anonymize' : False})
movie = imdb.find_movie_by_id("tt0382932")

def run_tests():
    global imdb

    print('actors have a name:')
    if movie.actors[0].name == 'Brad Garrett':
        print('passed')

    print('actors have a role:')
    if movie.actors[0].role == 'Gusteau':
        print('passed')

    print('directors have a name:')
    if movie.directors[0].name == 'Brad Bird':
        print('passed')

    print('directors do not have a role:')
    if movie.directors[0].role is None:
        print('passed')

    print('writers have a name:')
    if movie.writers[0].name == 'Brad Bird':
        print('passed')

    print('writers do not have a role:')
    if movie.writers[0].role is None:
        print('passed')



if __name__ == '__main__':
    run_tests()
