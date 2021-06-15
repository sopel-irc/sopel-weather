# coding=utf-8
import requests

from datetime import datetime


def darksky_forecast(bot, latitude, longitude, location):
    url = 'https://api.darksky.net/forecast/{}/{},{}'.format(
        bot.config.weather.weather_api_key,
        latitude,
        longitude
    )

    params = {
        'exclude': 'currently,minutely,hourly,alerts,flags',  # Exclude extra data we don't want/need
        'units': 'si'
    }
    try:
        r = requests.get(url, params=params)
    except:
        raise Exception("An Error Occurred. Check Logs For More Information.")
    data = r.json()
    if r.status_code != 200:
        raise Exception('Error: {}'.format(data['error']))
    else:
        weather_data = {'location': location, 'data': []}
        for day in data['daily']['data'][0:4]:
            weather_data['data'].append({
                'dow': datetime.fromtimestamp(day['time']).strftime('%A'),
                'summary': day['summary'].strip('.'),
                'high_temp': day['temperatureHigh'],
                'low_temp': day['temperatureLow']
            })
        return weather_data


def darksky_weather(bot, latitude, longitude, location):
    url = 'https://api.darksky.net/forecast/{}/{},{}'.format(
        bot.config.weather.weather_api_key,
        latitude,
        longitude
    )

    params = {
        'exclude': 'minutely,hourly,daily,alerts,flags',  # Exclude extra data we don't want/need
        'units': 'si'
    }
    try:
        r = requests.get(url, params=params)
    except:
        raise Exception("An Error Occurred. Check Logs For More Information.")
    data = r.json()
    if r.status_code != 200:
        raise Exception('Error: {}'.format(data['error']))
    else:
        weather_data = {
            'location': location,
            'temp': data['currently']['temperature'],
            'condition': data['currently']['summary'],
            'humidity': data['currently']['humidity'],
            'wind': {'speed': data['currently']['windSpeed'], 'bearing': data['currently']['windBearing']},
            'uvindex': data['currently']['uvIndex'],
            'timezone': data['timezone'],
        }

        if bot.config.weather.sunrise_sunset:
            weather_data['sunrise'] = data['currently']['sunriseTime']
            weather_data['sunset'] = data['currently']['sunsetTime']

        return weather_data
