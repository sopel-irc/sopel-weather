# coding=utf-8
import requests

from datetime import datetime


def openweathermap_forecast(bot, latitude, longitude, location):
    url = 'https://api.openweathermap.org/data/2.5/onecall?appid={}&lat={}&lon={}'.format(
        bot.config.weather.weather_api_key,
        latitude,
        longitude
    )

    params = {
        'exclude': 'current,minutely,hourly',
        'units': 'metric'
    }
    r = requests.get(url, params=params)
    data = r.json()
    if r.status_code != 200:
        raise Exception('Error: {}'.format(data['message']))
    else:
        weather_data = {'location': location, 'data': []}
        for day in data['daily'][0:4]:
            weather_data['data'].append({
                'dow': datetime.fromtimestamp(day['dt']).strftime('%A'),
                'summary': day['weather'][0]['main'],
                'high_temp': day['temp']['max'],
                'low_temp': day['temp']['min']
            })
        return weather_data


def openweathermap_weather(bot, latitude, longitude, location):
    url = 'https://api.openweathermap.org/data/2.5/onecall?appid={}&lat={}&lon={}'.format(
        bot.config.weather.weather_api_key,
        latitude,
        longitude
    )

    params = {
        'exclude': 'minutely,hourly,daily',
        'units': 'metric'
    }
    r = requests.get(url, params=params)
    data = r.json()
    print(data)
    if r.status_code != 200:
        raise Exception('Error: {}'.format(data['message']))
    else:
        weather_data = {
            'location': location,
            'temp': data['current']['temp'],
            'condition': data['current']['weather'][0]['main'],
            'humidity': float(data['current']['humidity'] / 100),  # Normalize this to decimal percentage
            'wind': {'speed': data['current']['wind_speed'], 'bearing': data['current']['wind_deg']},
        }
        return weather_data
