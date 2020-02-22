===============
 sopel-weather
===============

|version| |build| |issues| |alerts| |coverage-status| |license|

Introduction
============
sopel-weather is an weather lookup module for Sopel.

Since Yahoo deprecated their weather API on January 3, 2019, a reimplementation of the weather module was necessary 

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

LocationIQ


.. code-block::

    https://locationiq.com/

Dark Sky

.. code-block::

    https://darksky.net/

Python Requirements
~~~~~~~~~~~~~~~~~~~
.. code-block::

    requests
    sopel

.. |version| image:: https://img.shields.io/pypi/v/sopel-modules.weather.svg
   :target: https://pypi.python.org/pypi/sopel-modules.weather
.. |build| image:: https://travis-ci.com/RustyBower/sopel-weather.svg?branch=master
   :target: https://travis-ci.com/RustyBower/sopel-weather
.. |issues| image:: https://img.shields.io/github/issues/RustyBower/sopel-weather.svg
   :target: https://travis-ci.com/RustyBower/sopel-weather/issues
.. |alerts| image:: https://img.shields.io/lgtm/alerts/g/RustyBower/sopel-weather.svg
   :target: https://lgtm.com/projects/g/RustyBower/sopel-weather/alerts/
.. |coverage-status| image:: https://coveralls.io/repos/github/RustyBower/sopel-weather/badge.svg?branch=master
   :target: https://coveralls.io/github/RustyBower/sopel-weather?branch=master
.. |license| image:: https://img.shields.io/pypi/l/sopel-modules.weather.svg
   :target: https://github.com/RustyBower/sopel-modules.weather/blob/master/COPYING
