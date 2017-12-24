.. :changelog:

Release History
---------------

4.4.0 (2017-12-24)
++++++++++++++++++

- Fixes ``search_for_person`` and ``search_for_title`` methods, which were broken because XML api used by the client was removed, migrated to using search suggestions api used by the website itself.
- Adds optional ``session`` param to client init method, used to specify ``requests.Session``.
- All client methods will raise ``ValueError`` if invalid ``imdb_id`` param given.


4.3.0 (2017-08-10)
++++++++++++++++++

**Added**

- Added ``Imdb.popular_movies`` to retrieve current popular movies.


4.2.0 (2016-09-29)
++++++++++++++++++

**Added**

- ``Person.photo_url`` has been added. It returns a string (url) or None.


4.1.0 (2016-07-26)
++++++++++++++++++

- Changed ``Title`` and other objects to use less memory.
- Added notice of deprecation of caching in version 5.0.0.
- Added ``Imdb.get_episodes`` to retrieve Title Episode information.


4.0.2 (2015-08-08)
++++++++++++++++++

**Added**
- Added ``cache_expiry`` parameter to ``Imdb`` class, to specify cache expiry in seconds.

**Changes**

- Internal caching changed you use 3rd party package ``cachecontrol``.

**Removed**

- ``Imdb`` class no longer takes a ``cache_dir`` parameter.


3.0.0 (2015-06-12)
++++++++++++++++++

**Changed**

- All methods on ``Imdb`` will raise ``imdbpie.exceptions.HTTPError`` if a bad request to the API or resource is not found ("Errors should never pass silently").
- ``Imdb.get_title_reviews`` now has param `max_results` to limit number of reviews returned.


2.1.0 (2015-05-03)
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
