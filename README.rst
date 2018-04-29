**NOTICE**: If you're reading this on GitHub.com please be aware this is a mirror of the primary remote located at https://code.richard.do/richardARPANET/imdb-pie.
Please direct issues and pull requests there.

ImdbPie
=======

|PyPI| |Python Versions| |Build Status|

Python IMDB client using the IMDB JSON web service made available for their iOS application.

NOTICE: If you're reading this on Github.com please be aware this is a mirror of the primary remote located at https://code.richard.do/explore/projects.
Please direct any issues or pull requests Gitlab.

API Terminology
---------------

-  ``Title`` this can be a movie, tv show, video, documentary etc.
-  ``Name`` this can be a credit, cast member, any person generally.

Installation
------------

To install imdbpie, simply:

.. code:: bash

    pip install imdbpie

How To Use
----------

Initialise the client
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from imdbpie import Imdb
    imdb = Imdb()

Available methods
~~~~~~~~~~~~~~~~~

NOTE: For each client method, if the resource cannot be found they will
raise ``LookupError``, for any other API status codes > 399 the client will raise ``ImdbAPIError``.

+----------------------------------------------------------------+-----------------------------------+
| Example                                                        | Description                       |
+================================================================+===================================+
| ``get_title('tt0111161')``                                     | Returns a dict containing title   |
|                                                                | information                       |
+----------------------------------------------------------------+-----------------------------------+
| ``search_for_title("The Dark Knight")``                        | Returns a dict of results         |
|                                                                |                                   |
+----------------------------------------------------------------+-----------------------------------+
| ``search_for_name("Christian Bale")``                          | Returns a dict of results         |
|                                                                |                                   |
+----------------------------------------------------------------+-----------------------------------+
| ``title_exists('tt0111161')``                                  | Returns True if exists otherwise  |
|                                                                | False                             |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_genres('tt0303461')``                              | Returns a dict containing title   |
|                                                                | genres information                |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_credits('tt0303461')``                             | Returns a dict containing title   |
|                                                                | credits information               |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_quotes('tt0303461')``                              | Returns a dict containing title   |
|                                                                | quotes information                |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_ratings('tt0303461')``                             | Returns a dict containing title   |
|                                                                | ratings information               |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_connections('tt0303461')``                         | Returns a dict containing title   |
|                                                                | connections information           |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_similarities('tt0303461')``                        | Returns a dict containing title   |
|                                                                | similarities information          |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_videos('tt0303461')``                              | Returns a dict containing title   |
|                                                                | videos information                |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_news('tt0303461')``                                | Returns a dict containing news    |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_trivia('tt0303461')``                              | Returns a dict containing trivia  |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_soundtracks('tt0303461')``                         | Returns a dict containing         |
|                                                                | soundtracks information           |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_goofs('tt0303461')``                               | Returns a dict containing “goofs” |
|                                                                | and teaser information            |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_technical('tt0303461')``                           | Returns a dict containing         |
|                                                                | technical information             |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_companies('tt0303461')``                           | Returns a dict containing         |
|                                                                | information about companies       |
|                                                                | related to title                  |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_episodes('tt0303461')``                            | Returns a dict containing season  |
|                                                                | and episodes information          |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_episodes_detailed(imdb_id='tt0303461', season=1)`` | Returns a dict containing         |
|                                                                | detailed season episodes          |
|                                                                | information                       |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_top_crew('tt0303461')``                            | Returns a dict containing         |
|                                                                | detailed information about        |
|                                                                | title’s top crew (ie: directors,  |
|                                                                | writters, etc.)                   |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_plot('tt0111161')``                                | Returns a dict containing title   |
|                                                                | plot information                  |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_plot_synopsis('tt0111161')``                       | Returns a dict containing title   |
|                                                                | plot synopsis information         |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_awards('tt0111161')``                              | Returns a dict containing title   |
|                                                                | plot information                  |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_releases('tt0111161')``                            | Returns a dict containing         |
|                                                                | releases information              |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_versions('tt0111161')``                            | Returns a dict containing         |
|                                                                | versions information (meaning     |
|                                                                | different versions of this title  |
|                                                                | for different regions, or         |
|                                                                | different versions for DVD vs     |
|                                                                | Cinema)                           |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_user_reviews('tt0111161')``                        | Returns a dict containing user    |
|                                                                | review information                |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_metacritic_reviews('tt0111161')``                  | Returns a dict containing         |
|                                                                | metacritic review information     |
+----------------------------------------------------------------+-----------------------------------+
| ``get_title_images('tt0111161')``                              | Returns a dict containing title   |
|                                                                | images information                |
+----------------------------------------------------------------+-----------------------------------+
| ``get_name('nm0000151')``                                      | Returns a dict containing         |
|                                                                | person/name information           |
+----------------------------------------------------------------+-----------------------------------+
| ``get_name_filmography('nm0000151')``                          | Returns a dict containing         |
|                                                                | person/name filmography           |
|                                                                | information                       |
+----------------------------------------------------------------+-----------------------------------+
| ``get_name_images('nm0000032')``                               | Returns a dict containing         |
|                                                                | person/name images information    |
+----------------------------------------------------------------+-----------------------------------+
| ``get_name_videos('nm0000032')``                               | Returns a dict containing         |
|                                                                | person/name videos information    |
+----------------------------------------------------------------+-----------------------------------+
| ``validate_imdb_id('tt0111161')``                              | Raises ``ValueError`` if not      |
|                                                                | valid                             |
+----------------------------------------------------------------+-----------------------------------+
| ``get_popular_titles()``                                       | Returns a dict containing popular |
|                                                                | titles information                |
+----------------------------------------------------------------+-----------------------------------+
| ``get_popular_shows()``                                        | Returns a dict containing popular |
|                                                                | tv shows                          |
+----------------------------------------------------------------+-----------------------------------+
| ``get_popular_movies()``                                       | Returns a dict containing popular |
|                                                                | movies                            |
+----------------------------------------------------------------+-----------------------------------+

Requirements
------------

::

    1. Python 2 or 3
    2. See requirements.txt

Running the tests
-----------------

.. code:: bash

    pip install -r test_requirements.txt
    py.test src/tests

.. |PyPI| image:: https://img.shields.io/pypi/v/imdbpie.svg
   :target: https://pypi.python.org/pypi/imdb-pie
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/imdbpie.svg
   :target: https://pypi.python.org/pypi/imdb-pie
.. |Build Status| image:: https://travis-ci.org/richardARPANET/imdb-pie.png?branch=master
   :target: https://travis-ci.org/richardARPANET/imdb-pie
