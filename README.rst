ImdbPie
=======

|PyPI| |Python Versions|

Python IMDB client using the IMDB JSON web service made available for their iOS application.

API Terminology
---------------

-  ``Title`` this can be a movie, tv show, video, documentary etc.
-  ``Name`` this can be a credit, cast member, any person generally.

Installation
------------

To install imdbpie, simply:

.. code:: bash

    pip install imdbpie

How to use
------------

Choose an option:

1. `ImdbPie Facade usage examples <FACADE.rst>`_ (the easy way, returns objects).

2. `ImdbPie Client usage examples <CLIENT.rst>`_ (more low level client API, returns raw dicts).

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
