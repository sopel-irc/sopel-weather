===============
 sopel-weather
===============

|version| |build| |issues| |alerts| |coverage-status| |license|

Introduction
------------
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

24h Forecast
~~~~~~~~~~~~
.. code-block::

    .forecast # Only works if setlocation has been previously run
    .forecast seattle, us
    .forecast london

Customize User Location
~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

    .setlocation london # Sets location by city name
    .setlocation w2643743 # Sets location by WOEID (We are prepending w in front of WOEIDs because they collide with zips)
    .setlocation 98101 # Sets location by zip code

Requirements
============

API Key
~~~~~~~
.. code-block::

    https://openweathermap.org/api

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
