===============
 sopel-weather
===============

|version| |build| |issues| |alerts| |coverage-status| |license|

Introduction
============
sopel-weather is a weather lookup plugin for Sopel.

Since Yahoo deprecated their weather API on January 3, 2019, a reimplementation of the weather plugin was necessary 

Installing
==========

If possible, use ``pip`` to install this plugin. Below are example commands; you
might need to add ``sudo`` and/or call a different ``pip`` (e.g. ``pip3``) depending
on your system and environment. Do not use ``setup.py install``; Sopel won't be
able to load the plugin correctly.

Published release
~~~~~~~~~~~~~~~~~
.. code-block::

    pip install sopel-modules.weather

From source
~~~~~~~~~~~
Clone the repo, then run this in /path/to/sopel-weather

.. code-block::

    pip install .

Configuring
===========
You can automatically configure this plugin using the `sopel configure --plugins` command.

However, if you want or need to configure this plugin manually, you will need to define the following in `~/.sopel/default.cfg`

.. code-block::

    [weather]
    geocoords_provider = GEOCOORDS_PROVIDER
    geocoords_api_key = GEOCOORDS_API_KEY
    weather_provider = WEATHER_PROVIDER
    weather_api_key = WEATHER_API_KEY



Usage
=====

Current Weather
~~~~~~~~~~~~~~~
.. code-block::

    .weather # Only works if setlocation has been previously run
    .weather seattle, us
    .weather london

.. code-block::

    Paris, Ile-de-France, FR: 6°C (42°F), Clear, Humidity: 83%, UV Index: 0, Gentle breeze 4.0m/s (↗)

24h Forecast
~~~~~~~~~~~~
.. code-block::

    .forecast # Only works if setlocation has been previously run
    .forecast seattle, us
    .forecast london

.. code-block::

 Forecast: Paris, Ile-de-France, FR: Light rain tomorrow through next Saturday, High: 15°C (59°F), Low: 11°C (52°F), UV Index: 2

Customize User Location
~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

    .setlocation london # Sets location by city name
    .setlocation 98101 # Sets location by US zip code

.. code-block::

    I now have you at Paris, Ile-de-France, FR

Requirements
============

Modern weather APIs require Latitude & Longitude as inputs to their APIs, so we need to leverage a GeoCoords API to convert location searches to coordinates.

API Keys
~~~~~~~~

GeoCoords
*********
LocationIQ

.. code-block::

    https://locationiq.com/

Weather
*******
Dark Sky

.. code-block::

    https://darksky.net/

OpenWeatherMap

.. code-block::

    https://openweathermap.org/

Python Requirements
~~~~~~~~~~~~~~~~~~~
.. code-block::

    requests
    sopel

.. |version| image:: https://img.shields.io/pypi/v/sopel-modules.weather.svg
   :target: https://pypi.python.org/pypi/sopel-modules.weather
.. |build| image:: https://github.com/sopel-irc/sopel-weather/actions/workflows/python-tests.yml/badge.svg?branch=master
   :target: https://github.com/sopel-irc/sopel-weather/actions/workflows/python-tests.yml
.. |issues| image:: https://img.shields.io/github/issues/RustyBower/sopel-weather.svg
   :target: https://travis-ci.com/RustyBower/sopel-weather/issues
.. |alerts| image:: https://img.shields.io/lgtm/alerts/g/RustyBower/sopel-weather.svg
   :target: https://lgtm.com/projects/g/RustyBower/sopel-weather/alerts/
.. |coverage-status| image:: https://coveralls.io/repos/github/RustyBower/sopel-weather/badge.svg?branch=master
   :target: https://coveralls.io/github/RustyBower/sopel-weather?branch=master
.. |license| image:: https://img.shields.io/pypi/l/sopel-modules.weather.svg
   :target: https://github.com/RustyBower/sopel-modules.weather/blob/master/COPYING
