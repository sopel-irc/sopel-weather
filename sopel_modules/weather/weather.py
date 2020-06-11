# coding=utf-8
# Copyright 2008, Sean B. Palmer, inamidst.com
# Copyright 2012, Elsie Powell, embolalia.com
# Copyright 2018, Rusty Bower, rustybower.com
# Licensed under the Eiffel Forum License 2.
from __future__ import unicode_literals, absolute_import, print_function, division

import requests

from datetime import datetime

from sopel.config.types import NO_DEFAULT, ChoiceAttribute, StaticSection, ValidatedAttribute
from sopel.module import commands, example, NOLIMIT
from sopel.modules.units import c_to_f

from .providers.weather.darksky import darksky_forecast, darksky_weather
from .providers.weather.openweathermap import openweathermap_forecast, openweathermap_weather

WEATHER_PROVIDERS = [
    'darksky',
    'openweathermap',
]


# Define our sopel weather configuration
class WeatherSection(StaticSection):
    geocoords_provider = ValidatedAttribute('geocoords_provider', str, default='locationiq')
    geocoords_api_key = ValidatedAttribute('geocoords_api_key', str, default='')
    weather_provider = ChoiceAttribute('weather_provider', WEATHER_PROVIDERS, default=NO_DEFAULT)
    weather_api_key = ValidatedAttribute('weather_api_key', str, default='')


def setup(bot):
    bot.config.define_section('weather', WeatherSection)


# Walk the user through defining variables required
def configure(config):
    config.define_section('weather', WeatherSection, validate=False)
    config.weather.configure_setting(
        'geocoords_provider',
        'Enter GeoCoords API Provider:',
        default=NO_DEFAULT
    )
    config.weather.configure_setting(
        'geocoords_api_key',
        'Enter GeoCoords API Key:',
        default=NO_DEFAULT
    )
    config.weather.configure_setting(
        'weather_provider',
        'Enter Weather API Provider: ({}):'.format(', '.join(WEATHER_PROVIDERS)),
        default=NO_DEFAULT
    )
    config.weather.configure_setting(
        'weather_api_key',
        'Enter Weather API Key:',
        default=NO_DEFAULT
    )


def get_temp(temp):
    try:
        temp = float(temp)
    except (KeyError, TypeError, ValueError):
        return 'unknown'
    return u'%d\u00B0C (%d\u00B0F)' % (round(temp), round(c_to_f(temp)))


def get_humidity(humidity):
    try:
        humidity = int(humidity * 100)
    except (KeyError, TypeError, ValueError):
        return 'unknown'
    return "Humidity: %s%%" % humidity


def get_wind(speed, bearing):
    m_s = float(round(speed, 1))
    speed = int(round(m_s * 1.94384, 0))
    bearing = int(bearing)

    if speed < 1:
        description = 'Calm'
    elif speed < 4:
        description = 'Light air'
    elif speed < 7:
        description = 'Light breeze'
    elif speed < 11:
        description = 'Gentle breeze'
    elif speed < 16:
        description = 'Moderate breeze'
    elif speed < 22:
        description = 'Fresh breeze'
    elif speed < 28:
        description = 'Strong breeze'
    elif speed < 34:
        description = 'Near gale'
    elif speed < 41:
        description = 'Gale'
    elif speed < 48:
        description = 'Strong gale'
    elif speed < 56:
        description = 'Storm'
    elif speed < 64:
        description = 'Violent storm'
    else:
        description = 'Hurricane'

    if (bearing <= 22.5) or (bearing > 337.5):
        bearing = u'\u2193'
    elif (bearing > 22.5) and (bearing <= 67.5):
        bearing = u'\u2199'
    elif (bearing > 67.5) and (bearing <= 112.5):
        bearing = u'\u2190'
    elif (bearing > 112.5) and (bearing <= 157.5):
        bearing = u'\u2196'
    elif (bearing > 157.5) and (bearing <= 202.5):
        bearing = u'\u2191'
    elif (bearing > 202.5) and (bearing <= 247.5):
        bearing = u'\u2197'
    elif (bearing > 247.5) and (bearing <= 292.5):
        bearing = u'\u2192'
    elif (bearing > 292.5) and (bearing <= 337.5):
        bearing = u'\u2198'

    return description + ' ' + str(m_s) + 'm/s (' + bearing + ')'


def get_geocoords(bot, trigger):
    url = "https://us1.locationiq.com/v1/search.php"  # This can be updated to their EU endpoint for EU users
    data = {
        'key': bot.config.weather.geocoords_api_key,
        'q': trigger.group(2),
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }
    r = requests.get(url, params=data)
    if r.status_code != 200:
        raise Exception(r.json()['error'])

    latitude = r.json()[0]['lat']
    longitude = r.json()[0]['lon']
    address = r.json()[0]['address']

    # Zip codes give us town versus city
    if 'city' in address.keys():
        location = '{}, {}, {}'.format(address['city'],
                                       address['state'],
                                       address['country_code'].upper())
    elif 'town' in address.keys():
        location = '{}, {}, {}'.format(address['town'],
                                       address['state'],
                                       address['country_code'].upper())
    elif 'county' in address.keys():
        location = '{}, {}, {}'.format(address['county'],
                                       address['state'],
                                       address['country_code'].upper())
    elif 'city_district' in address.keys():
        location = '{}, {}'.format(address['city_district'],
                                   address['country_code'].upper())
    else:
        location = 'Unknown'

    return latitude, longitude, location


# 24h Forecast: Oshkosh, US: Broken Clouds, High: 0°C (32°F), Low: -7°C (19°F)
def get_forecast(bot, trigger):
    location = trigger.group(2)
    if not location:
        latitude = bot.db.get_nick_value(trigger.nick, 'latitude')
        longitude = bot.db.get_nick_value(trigger.nick, 'longitude')
    else:
        latitude, longitude, location = get_geocoords(bot, trigger)

    # DarkSky
    if bot.config.weather.weather_provider == 'darksky':
        return darksky_forecast(bot, latitude, longitude, location)
    # OpenWeatherMap
    elif bot.config.weather.weather_provider == 'openweathermap':
        return openweathermap_forecast(bot, latitude, longitude, location)
    # Unsupported Provider
    else:
        raise Exception('Error: Unsupported Provider')


def get_weather(bot, trigger):
    location = trigger.group(2)
    if not location:
        latitude = bot.db.get_nick_value(trigger.nick, 'latitude')
        longitude = bot.db.get_nick_value(trigger.nick, 'longitude')
    else:
        latitude, longitude, location = get_geocoords(bot, trigger)

    # DarkSky
    if bot.config.weather.weather_provider == 'darksky':
        return darksky_weather(bot, latitude, longitude, location)
    # OpenWeatherMap
    elif bot.config.weather.weather_provider == 'openweathermap':
        return openweathermap_weather(bot, latitude, longitude, location)
    # Unsupported Provider
    else:
        raise Exception('Error: Unsupported Provider')


@commands('weather', 'wea')
@example('.weather')
@example('.weather London')
@example('.weather Seattle, US')
@example('.weather 90210')
def weather_command(bot, trigger):
    """.weather location - Show the weather at the given location."""
    if bot.config.weather.weather_api_key is None or bot.config.weather.weather_api_key == '':
        return bot.reply("Weather API key missing. Please configure this module.")
    if bot.config.weather.geocoords_api_key is None or bot.config.weather.geocoords_api_key == '':
        return bot.reply("GeoCoords API key missing. Please configure this module.")

    # Ensure we have a location for the user
    location = trigger.group(2)
    if not location:
        latitude = bot.db.get_nick_value(trigger.nick, 'latitude')
        longitude = bot.db.get_nick_value(trigger.nick, 'longitude')
        if not latitude or not longitude:
            return bot.say("I don't know where you live. "
                           "Give me a location, like {pfx}{command} London, "
                           "or tell me where you live by saying {pfx}setlocation "
                           "London, for example.".format(command=trigger.group(1),
                                                         pfx=bot.config.core.help_prefix))

    data = get_weather(bot, trigger)
    weather = u'{location}: {temp}, {condition}, {humidity}'.format(
        location=data['location'],
        temp=get_temp(data['temp']),
        condition=data['condition'],
        humidity=get_humidity(data['humidity'])
    )
    # Some providers don't give us UV Index
    if 'uvindex' in data.keys():
        weather += ', UV Index: {uvindex}'.format(uvindex=data['uvindex'])
    weather += ', {wind}'.format(wind=get_wind(data['wind']['speed'], data['wind']['bearing']))
    return bot.say(weather)


@commands('forecast')
@example('.forecast')
@example('.forecast London')
@example('.forecast Seattle, US')
@example('.forecast 90210')
def forecast_command(bot, trigger):
    """.forecast location - Show the weather forecast for tomorrow at the given location."""
    if bot.config.weather.weather_api_key is None or bot.config.weather.weather_api_key == '':
        return bot.reply("Weather API key missing. Please configure this module.")
    if bot.config.weather.geocoords_api_key is None or bot.config.weather.geocoords_api_key == '':
        return bot.reply("GeoCoords API key missing. Please configure this module.")
    data = get_forecast(bot, trigger)
    forecast = '{location}'.format(location=data['location'])
    for day in data['data']:
        forecast += ' :: {dow} - {summary} - {high_temp} / {low_temp}'.format(
            dow=day.get('dow'),
            summary=day.get('summary'),
            high_temp=get_temp(day.get('high_temp')),
            low_temp=get_temp(day.get('low_temp'))
        )
    return bot.say(forecast)


@commands('setlocation')
@example('.setlocation London')
@example('.setlocation Seattle, US')
@example('.setlocation 90210')
@example('.setlocation w7174408')
def update_location(bot, trigger):
    if bot.config.weather.geocoords_api_key is None or bot.config.weather.geocoords_api_key == '':
        return bot.reply("GeoCoords API key missing. Please configure this module.")

    # Return an error if no location is provided
    if not trigger.group(2):
        bot.reply('Give me a location, like "London" or "90210".')
        return NOLIMIT

    # Get GeoCoords
    latitude, longitude, location = get_geocoords(bot, trigger)

    # Assign Latitude & Longitude to user
    bot.db.set_nick_value(trigger.nick, 'latitude', latitude)
    bot.db.set_nick_value(trigger.nick, 'longitude', longitude)
    bot.db.set_nick_value(trigger.nick, 'location', location)

    return bot.reply('I now have you at {}'.format(location))
