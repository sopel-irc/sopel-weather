# coding=utf-8
# Copyright 2008, Sean B. Palmer, inamidst.com
# Copyright 2012, Elsie Powell, embolalia.com
# Copyright 2018, Rusty Bower, rustybower.com
# Licensed under the Eiffel Forum License 2.
from __future__ import unicode_literals, absolute_import, print_function, division

from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.module import commands, example, NOLIMIT
from sopel.modules.units import c_to_f

import re
import requests


# Define our sopel weather configuration
class WeatherSection(StaticSection):
    api_key = ValidatedAttribute('api_key', str, default='')


def setup(bot):
    bot.config.define_section('weather', WeatherSection)


# Walk the user through defining variables required
def configure(config):
    config.define_section('weather', WeatherSection, validate=False)
    config.weather.configure_setting(
        'api_key',
        'Enter openweathermap.org API Key:'
    )


def location_search(location, api_key):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    results = requests.get('https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric' % (location, api_key))
    if results is None or results.status_code is not 200:
        return None
    return results.json()


def woeid_search(woeid, api_key):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    results = requests.get('https://api.openweathermap.org/data/2.5/weather?id=%s&appid=%s&units=metric' % (woeid, api_key))
    if results is None or results.status_code is not 200:
        return None
    return results.json()


def zip_search(zip_code, api_key):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    results = requests.get('https://api.openweathermap.org/data/2.5/weather?zip=%s&appid=%s&units=metric' % (zip_code, api_key))
    if results is None or results.status_code is not 200:
        return None
    return results.json()


def get_temp(parsed):
    try:
        temp = int(parsed['main']['temp'])
    except (KeyError, ValueError):
        return 'unknown'
    return u'%d\u00B0C (%d\u00B0F)' % (temp, c_to_f(temp))


def get_humidity(parsed):
    try:
        humidity = parsed['main']['humidity']
    except (KeyError, ValueError):
        return 'unknown'
    return "Humidity: %s%%" % humidity


def get_wind(parsed):
    try:
        wind_data = parsed['wind']
        m_s = float(round(wind_data['speed'], 1))
        speed = int(round(m_s * 1.94384, 0))
        degrees = int(wind_data['deg'])
    except (KeyError, ValueError):
        return 'unknown'

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

    if (degrees <= 22.5) or (degrees > 337.5):
        degrees = u'\u2193'
    elif (degrees > 22.5) and (degrees <= 67.5):
        degrees = u'\u2199'
    elif (degrees > 67.5) and (degrees <= 112.5):
        degrees = u'\u2190'
    elif (degrees > 112.5) and (degrees <= 157.5):
        degrees = u'\u2196'
    elif (degrees > 157.5) and (degrees <= 202.5):
        degrees = u'\u2191'
    elif (degrees > 202.5) and (degrees <= 247.5):
        degrees = u'\u2197'
    elif (degrees > 247.5) and (degrees <= 292.5):
        degrees = u'\u2192'
    elif (degrees > 292.5) and (degrees <= 337.5):
        degrees = u'\u2198'

    return description + ' ' + str(m_s) + 'm/s (' + degrees + ')'


def say_info(bot, trigger):
    location = trigger.group(2)
    woeid = ''
    if not location:
        woeid = bot.db.get_nick_value(trigger.nick, 'woeid')
        if not woeid:
            return bot.reply("I don't know where you live. "
                             "Give me a location, like {pfx}{command} London, "
                             "or tell me where you live by saying {pfx}setlocation "
                             "London, for example.".format(command=trigger.group(1),
                                                           pfx=bot.config.core.help_prefix))
    else:
        location = location.strip()
        woeid = bot.db.get_nick_value(location, 'woeid')
        if woeid is None:
            # Check if WOEID
            if re.match(r'^w\d+$', trigger.group(2)):
                # Pop off the w from our trigger.group
                result = woeid_search(trigger.group(2)[1:], bot.config.weather.api_key)
            # Check if zip code (this doesn't cover all, but most)
            # https://en.wikipedia.org/wiki/List_of_postal_codes
            elif re.match(r'^\d+$', trigger.group(2)):
                result = zip_search(trigger.group(2), bot.config.weather.api_key)
            # Otherwise, we assume it's a city name
            else:
                result = location_search(trigger.group(2), bot.config.weather.api_key)
            if not result:
                return bot.reply("I don't know where that is.")

            woeid = result['id']

    if not woeid:
        return bot.reply("I don't know where that is.")

    result = woeid_search(woeid, bot.config.weather.api_key)

    if not result:
        return bot.reply("An error occurred")
    else:
        location = result['name']
        country = result['sys']['country']
        temp = get_temp(result)
        humidity = get_humidity(result)
        wind = get_wind(result)
        return bot.say(u'%s, %s: %s, %s, %s' % (location, country, temp, humidity, wind))


@commands('weather', 'wea')
@example('.weather London')
@example('.weather Seattle')
def weather_command(bot, trigger):
    """.weather location - Show the weather at the given location."""
    if bot.config.weather.api_key is None or bot.config.weather.api_key is '':
        return bot.reply("OpenWeatherMap API key missing. Please configure this module.")
    say_info(bot, trigger)


@commands('setlocation')
@example('.setlocation London')
@example('.setlocation 90210')
@example('.setlocation w7174408')
def update_location(bot, trigger):
    """Set your default weather location."""
    if not trigger.group(2):
        bot.reply('Give me a location, like "London" or "90210" or "w2643743".')
        return NOLIMIT

    # Check if WOEID
    if re.match(r'^w\d+$', trigger.group(2)):
        # Pop off the w from our trigger.group
        result = woeid_search(trigger.group(2)[1:], bot.config.weather.api_key)
    # Check if zip code (this doesn't cover all, but most)
    # https://en.wikipedia.org/wiki/List_of_postal_codes
    elif re.match(r'^\d+$', trigger.group(2)):
        result = zip_search(trigger.group(2), bot.config.weather.api_key)
    # Otherwise, we assume it's a city name
    else:
        result = location_search(trigger.group(2), bot.config.weather.api_key)

    if not result:
        return bot.reply("I don't know where that is.")

    woeid = result['id']

    bot.db.set_nick_value(trigger.nick, 'woeid', woeid)

    city = result['name']
    country = result['sys']['country'] or ''
    bot.reply('I now have you at WOEID %s (%s, %s)' %
              (woeid, city, country))
