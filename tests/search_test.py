from imdbpie import Imdb

imdb = Imdb({'anonymize' : False})

def run_tests():
    print('search for title:')
    results = imdb.find_by_title("batman")
    print('should have minimum 15 results: ')
    print(len(results))


    print('search for title that has spaces:')
    results = imdb.find_by_title("the truman show")
    print('should have minimum 1 results: ')
    print(len(results))

    print('search for bad title with no results:')
    results = imdb.find_by_title("fdlfj494llsidjg49hkdg")
    print('should have 0 results: ')
    print(len(results))

    print('find movie by id:')
    results = imdb.find_movie_by_id("tt0382932")
    print('should be of class Imdb_Pie.Movie: ')
    print(type(results))

    print('find top 250 movies:')
    movies = imdb.top_250()
    print('should an list of dict(): ')
    print(type(movies))
    print(type(movies[0]))
    print(movies[0]['title'])

    print('find popular shows:')
    shows = imdb.popular_shows()
    print('should an list of dict(): ')
    print(type(shows))
    print(type(shows[0]))
    print(shows[0]['title'])

if __name__ == '__main__':
    run_tests()
