# Release History

5.4.3 (unreleased)
------------------

- Nothing changed yet.


5.4.2 (2018-04-05)
------------------

- Fixes missing setuptools dependency for pypi display of markdown formatted files.


5.4.1 (2018-04-05)
------------------

-   Packaging documentation fixes.

5.4.0 (2018-03-18)
------------------

-   Bugfix for incorrect AttributeError message showing when undefined
    attrs called on client class.
-   Adds `get_title_top_crew` method.

5.3.0 (2018-02-27)
------------------

-   Adds `get_title_plot_taglines` method.
-   Adds `get_title_news` method.
-   Adds `get_title_trivia` method.
-   Adds `get_title_soundtracks` method.
-   Adds `get_title_goofs` method.
-   Adds `get_title_technical` method.
-   Adds `get_title_companies` method.
-   Adds `get_title_episodes_detailed` method.

5.2.0 (2018-01-11)
------------------

-   Updates `get_title` to call "/auxiliary" as "/fulldetails" endpoint
    now returns an error.
-   Adds `get_title_quotes` method.
-   Adds `get_title_ratings` method.
-   Adds `get_title_connections` method.
-   Adds `get_title_awards` method.
-   Adds `get_title_plot_synopsis` method.
-   Adds `get_title_versions` method.
-   Adds `get_title_releases` method.
-   Adds `get_title_similarities` method.
-   Adds `get_title_videos` method.
-   Adds `get_name_videos` method.
-   Adds `get_name_filmography` method.
-   Adds response status code to `ImdbAPIError` exception message.

5.1.0 (2018-01-10)
------------------

-   Adds `get_title_genres` method.

5.0.0 (2018-01-10)
------------------

-   Fixes client to work with new API.
-   Renames most of methods on `Imdb` class.
-   Changes all methods on `Imdb` to return raw JSON resource dictionary
    rather than Python objects.
-   Removes params from `Imdb` `__init__` method (user\_agent,
    proxy\_uri, verify\_ssl, api\_key, cache, anonymize).
-   Adds `clear_cached_credentials` method to `Imdb` class.

4.4.2 (2018-01-03)
------------------

-   Fixes bug when searching with non alphanumeric characters, second
    attempt.

4.4.1 (2017-12-27)
------------------

-   Fixes bug when searching with non alphanumeric characters.

4.4.0 (2017-12-24)
------------------

-   Fixes `search_for_person` and `search_for_title` methods, which were
    broken because XML api used by the client was removed, migrated to
    using search suggestions api used by the website itself.
-   Adds optional `session` param to client init method, used to specify
    `requests.Session`.
-   All client methods will raise `ValueError` if invalid `imdb_id`
    param given.

4.3.0 (2017-08-10)
------------------

**Added**

-   Added `Imdb.popular_movies` to retrieve current popular movies.

4.2.0 (2016-09-29)
------------------

**Added**

-   `Person.photo_url` has been added. It returns a string (url) or
    None.

4.1.0 (2016-07-26)
------------------

-   Changed `Title` and other objects to use less memory.
-   Added notice of deprecation of caching in version 5.0.0.
-   Added `Imdb.get_episodes` to retrieve Title Episode information.

4.0.2 (2015-08-08)
------------------

**Added** - Added `cache_expiry` parameter to `Imdb` class, to specify
cache expiry in seconds.
