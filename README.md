[![PyPI version](https://badge.fury.io/py/sopel-modules.weather.svg)](https://badge.fury.io/py/sopel-modules.weather)
[![Build Status](https://travis-ci.org/RustyBower/sopel-weather.svg?branch=master)](https://travis-ci.org/RustyBower/sopel-weather)
[![Coverage Status](https://coveralls.io/repos/github/RustyBower/sopel-weather/badge.svg?branch=master)](https://coveralls.io/github/RustyBower/sopel-weather?branch=master)

# sopel-weather
sopel-weather is an weather lookup module for Sopel.

Since Yahoo deprecated their weather API on January 3, 2019, a reimplementation of the weather module was necessary 

## Usage
```
# Allows the user to set their current location
.setlocation london # Sets location by city name
.setlocation w2643743 # Sets location by WOEID (We are prepending w in front of WOEIDs because they collide with zips)
.setlocation 98101 # Sets location by zip code

# Gets a 24h forecast
.forecast # Only works if setlocation has been previously run
.forecast seattle, us
.forecast london

# Gets the current weather
.weather # Only works if setlocation has been previously run
.weather seattle, us
.weather london
```

## Requirements
#### API Key
```
https://openweathermap.org/api
```

#### Python Requirements
```
requests
sopel
```
