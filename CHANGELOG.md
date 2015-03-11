# Version 2

Title.runtime is now in seconds rather than minutes
Title.trailer_img_url is now gone
Title.trailer_img_urls returns a list of trailer images
Title.plots now contains list of plots
Title.plot_outline is removed
Title.trailers is now a list of dict with keys: url, format
Title.runtime is now in seconds rather than hours
Imdb.validate_id is gone
Imdb.movie_exists -> Imdb.title_exists
Imdb.title_reviews kwarg 'limit' is gone
Imdb.find_movie_by_id -> Imdb.get_title_by_id
Imdb.find_by_title -> Imdb.search_for_title
new Imdb.search_for_person
Imdb.title_images renamed to Imdb.get_title_images
Imdb.title_reviews -> Imdb.get_title_reviews
Imdb.person_images -> Imdb.get_person_images
Imdb.get_title_plots added

Person.role is now Person.roles and returns a list of string
