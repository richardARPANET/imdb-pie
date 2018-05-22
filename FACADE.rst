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

-  certification
-  creators
-  credits
-  directors
-  episode
-  episodes
-  genres
-  image
-  imdb_id
-  plot_outline
-  rating
-  rating_count
-  release_date
-  releases
-  season
-  stars
-  title
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
- image
- imdb_id
- name

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
