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

    uv add imdbpie

How to use
------------

Choose an option:

1. `ImdbPie Facade usage examples <FACADE.rst>`_ (the easy way, returns objects).

2. `ImdbPie Client usage examples <CLIENT.rst>`_ (more low level client API, returns raw dicts).

Requirements
------------

::

    1. Python 3.10 or newer
    2. Dependencies are declared in pyproject.toml and pinned in uv.lock

Development
-----------

This project uses `uv <https://docs.astral.sh/uv/>`_ for environments,
dependencies and locking.

.. code:: bash

    uv sync

Running the tests
-----------------

.. code:: bash

    uv run pytest src/tests

Some tests call the live IMDb API and are marked ``live``. Skip them when
working offline:

.. code:: bash

    uv run pytest src/tests -m "not live"

.. |PyPI| image:: https://img.shields.io/pypi/v/imdbpie.svg
   :target: https://pypi.python.org/pypi/imdb-pie
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/imdbpie.svg
   :target: https://pypi.python.org/pypi/imdb-pie
