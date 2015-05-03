.. :changelog:

Release History
---------------

2.0.2 (unreleased)
++++++++++++++++++
**Added**
- Added verify_ssl kwarg option to ``Imdb`` object. Allows for controlling of ssl cert verification on all requests made.


2.0.1 (2015-03-30)
++++++++++++++++++
**Added**

- ``Title.plot_outline`` has been added. It returns a string.


2.0.0 (2015-03-12)
++++++++++++++++++
**Added**

- ``Imdb.search_for_person`` has been added. It returns a list of dicts.
- ``Imdb.get_title_plots`` has been added. It returns a list of strings.
- ``Title.trailer_image_urls`` returns a list of trailer urls (string).
- ``Imdb.get_person_by_id`` has been added. It returns a Person object.

**Changed**

- ``Title.plots`` returns a list of *full* plots.
- ``Title.trailers`` returns a list of dicts (keys: "url", "format").
- ``Title.runtime`` returns runtime in seconds now instead of hours.
- ``Person.role`` is now ``Person.roles`` and returns a list rather than a string.
- ``Imdb.person_images`` has been renamed to ``Imdb.get_person_images``.
- ``Imdb.title_reviews`` has been renamed to ``Imdb.get_title_reviews`` and parameter ``limit`` has also been removed.
- ``Imdb.title_images`` has been renamed to ``Imdb.get_title_images``.
- ``Imdb.find_by_title`` has been renamed to ``Imdb.search_for_title``.
- ``Imdb.find_movie_by_id`` has been renamed to ``Imdb.get_title_by_id`` and parameter ``json`` has been removed.
- ``Imdb.movie_exists`` has been renamed to ``Imdb.title_exists``.

**Removed**

- ``Imdb.validate_id`` has been removed.
- ``Title.plot_outline`` has been removed.
- ``Title.trailer_img_url`` has been removed.

1.5.6 (2014-12-07)
++++++++++++++++++

- No notes, release made before changelog inception.
