from imdbpie import Imdb


def test():
    imdb = Imdb({'anonymize': False})
    title = imdb.find_movie_by_id("tt0096697")
    
   # for w in title.writers:
   #     print w.name

    #print len(title.writers)
    #72
    num_p = 0
    for person in title.credits:
        if person.token == 'writers':
            #print person
            num_p += 1
    print num_p
    print len(title.credits)

    return None


if __name__ == '__main__':
    print test()