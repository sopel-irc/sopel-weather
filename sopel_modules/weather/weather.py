# coding=utf-8
# Copyright 2008, Sean B. Palmer, inamidst.com
# Copyright 2012, Elsie Powell, embolalia.com
# Copyright 2018, Rusty Bower, rustybower.com
# Licensed under the Eiffel Forum License 2.
from __future__ import unicode_literals, absolute_import, print_function, division

from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.module import commands, example, NOLIMIT
from sopel.modules.units import c_to_f

import requests


# Define our sopel weather configuration
class WeatherSection(StaticSection):
    geocoords_provider = ValidatedAttribute('geocoords_provider', str, default='LocationIQ')
    geocoords_api_key = ValidatedAttribute('geocoords_api_key', str, default='')
    weather_provider = ValidatedAttribute('weather_provider', str, default='DarkSky')
    weather_api_key = ValidatedAttribute('weather_api_key', str, default='')


def setup(bot):
    bot.config.define_section('weather', WeatherSection)


# Walk the user through defining variables required
def configure(config):
    config.define_section('weather', WeatherSection, validate=False)
    config.weather.configure_setting(
        'geocoords_provider',
        'Enter GeoCoords API Key:'
    )
    config.weather.configure_setting(
        'geocoords_api_key',
        'Enter GeoCoords API Key:'
    )
    config.weather.configure_setting(
        'weather_provider',
        'Enter Weather API Provider:'
    )
    config.weather.configure_setting(
        'weather_api_key',
        'Enter Weather API Key:'
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
        location = bot.db.get_nick_value(trigger.nick, 'location')
        if not latitude and not longitude:
            return "I don't know where you live. " \
                   "Give me a location, like {pfx}{command} London, " \
                   "or tell me where you live by saying {pfx}setlocation " \
                   "London, for example.".format(command=trigger.group(1),
                                                 pfx=bot.config.core.help_prefix)
    else:
        latitude, longitude, location = get_geocoords(bot, trigger)

    # Query DarkSky
    url = 'https://api.darksky.net/forecast/{}/{},{}'.format(
        bot.config.weather.weather_api_key,
        latitude,
        longitude
    )
    data = {
        'exclude': 'currently,minutely,hourly,alerts,flags',  # Exclude extra data we don't want/need
        'units': 'si'
    }
    r = requests.get(url, params=data)
    data = r.json()
    if r.status_code != 200:
        return 'Error: {}'.format(data['error'])
    else:
        condition = data['daily']['summary'].strip('.')  # Remove strange period at end of summary
        high_temp = get_temp(data['daily']['data'][0]['temperatureHigh'])
        low_temp = get_temp(data['daily']['data'][0]['temperatureLow'])
        uvindex = data['daily']['data'][0]['uvIndex']
        # 24h Forecast: Oshkosh, US: Broken Clouds, High: 0°C (32°F), Low: -7°C (19°F)
        return u'Forecast: %s: %s, High: %s, Low: %s, UV Index: %s' % (location,
                                                                       condition,
                                                                       high_temp,
                                                                       low_temp,
                                                                       uvindex)


def get_weather(bot, trigger):
    location = trigger.group(2)
    if not location:
        latitude = bot.db.get_nick_value(trigger.nick, 'latitude')
        longitude = bot.db.get_nick_value(trigger.nick, 'longitude')
        location = bot.db.get_nick_value(trigger.nick, 'location')
        if not latitude and not longitude:
            return "I don't know where you live. " \
                   "Give me a location, like {pfx}{command} London, " \
                   "or tell me where you live by saying {pfx}setlocation " \
                   "London, for example.".format(command=trigger.group(1),
                                                 pfx=bot.config.core.help_prefix)
    else:
        latitude, longitude, location = get_geocoords(bot, trigger)

    # Query DarkSky
    url = 'https://api.darksky.net/forecast/{}/{},{}'.format(
        bot.config.weather.weather_api_key,
        latitude,
        longitude
    )
    data = {
        'exclude': 'minutely,hourly,daily,alerts,flags',  # Exclude extra data we don't want/need
        'units': 'si'
    }
    r = requests.get(url, params=data)
    data = r.json()
    if r.status_code != 200:
        return 'Error: {}'.format(data['error'])
    else:
        temp = get_temp(data['currently']['temperature'])
        condition = data['currently']['summary']
        humidity = get_humidity(data['currently']['humidity'])
        wind = get_wind(data['currently']['windSpeed'], data['currently']['windBearing'])
        uvindex = data['currently']['uvIndex']
        return u'%s: %s, %s, %s, UV Index: %s, %s' % (location, temp, condition, humidity, uvindex, wind)


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
    return bot.say(get_weather(bot, trigger))


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
    return bot.say(get_forecast(bot, trigger))


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
