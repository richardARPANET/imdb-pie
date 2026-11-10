ImdbPie Facade Usage Examples
=============================

Init the Facade
---------------

.. code:: python

   from imdbpie import ImdbFacade
   imdb = ImdbFacade()
   # Or, Specify a custom imdb-pie client instance for the facade to use
   from imdbpie import Imdb
   client = Imdb(locale='en_US')
   imdb = ImdbFacade(client=client)


Exceptions
----------

For each method, if the resource cannot be found they will raise ``LookupError``,
for any other API status codes > 399 the client will raise ``ImdbAPIError``.

Get a title
-----------

.. code:: python

   imdb.get_title(imdb_id='tt1023114')

Returns a ``Title`` object with the following attributes:

-  alternate_titles
-  alternate_titles_count
-  awards_summary
-  certificate_reason
-  certification
-  countries
-  creators
-  credits
-  directors
-  episode
-  episodes
-  genres
-  image
-  imdb_id
-  metacritic
-  plot_outline
-  production_status
-  rating
-  rating_count
-  release_date
-  releases
-  runtime
-  season
-  spoken_languages
-  stars
-  title
-  top_rank
-  trailer
-  type
-  writers
-  year

Get a Name
----------

.. code:: python

   imdb.get_name(imdb_id='nm0000151')

Returns a ``Name`` object with the following attributes:

- bios
- birth_place
- date_of_birth
- filmography
- gender
- height_centimeters
- image
- imdb_id
- jobs
- known_for
- name
- real_name

Note that ``date_of_birth``, ``gender`` and ``birth_place`` are ``None``
when IMDb does not publish them.

Search for a name
-----------------

.. code:: python

   imdb.search_for_name('Tom Hanks')

Returns a ``tuple`` containing ``NameSearchResult`` objects with the
following attributes:

-  imdb_id
-  name

Search for a title
------------------

.. code:: python

   imdb.search_for_title('The Dark Knight')

Returns a ``tuple`` containing ``TitleSearchResult`` objects with the
following attributes:

-  imdb_id
-  title
-  type
-  year

Get a title's watch options
---------------------------

.. code:: python

   imdb.get_title_watch_options('tt0111161')

Returns a ``tuple`` containing ``WatchOption`` objects with the following
attributes:

-  category
-  notes
-  provider
-  provider_id
-  url

``category`` is ``streaming``, ``rent/buy`` or another group IMDb returns.

Get a title's box office
------------------------

.. code:: python

   imdb.get_title_business('tt0111161')

Returns a ``TitleBusiness`` object with the following attributes:

-  budget
-  gross
-  opening_weekend_gross
-  worldwide_gross

``budget`` and ``worldwide_gross`` are dicts of ``amount`` and ``currency``.
``gross`` and ``opening_weekend_gross`` are tuples of the API's regional
dicts, which mix currencies and should be matched on ``region``.

Get a title's keywords
----------------------

.. code:: python

   imdb.get_title_keywords('tt0111161')

Returns a ``tuple`` of keyword strings.

Get a title's certificates
--------------------------

.. code:: python

   imdb.get_title_certificates('tt0111161')

Returns a ``tuple`` containing ``TitleCertificate`` objects with the
following attributes:

-  attributes
-  certificate
-  country

Get a title's filming locations
-------------------------------

.. code:: python

   imdb.get_title_filming_locations('tt0111161')

Returns a ``tuple`` containing ``FilmingLocation`` objects with the following
attributes:

-  attributes
-  location
-  notes

Get a title's crazy credits
---------------------------

.. code:: python

   imdb.get_title_crazy_credits('tt0111161')

Returns a ``tuple`` of strings.

Get a title's principals
------------------------

.. code:: python

   imdb.get_title_principals('tt0111161')

Returns a ``tuple`` of ``TitleName`` objects, including ``characters`` for
cast members.

Get a name's known for titles
-----------------------------

.. code:: python

   imdb.get_name_known_for('nm0000151')

Returns a ``tuple`` of imdb ids, in the same style as ``Name.filmography``.

Get a name's awards
-------------------

.. code:: python

   imdb.get_name_awards('nm0000151')

Returns a ``tuple`` containing ``Award`` objects with the following
attributes:

-  category
-  event_name
-  name
-  title_ids
-  won
-  year
