# coding=utf-8
import requests

from datetime import datetime


API_ENDPOINT = 'https://api.open-meteo.com/v1/forecast'

# Below from open-meteo's API docs; presumably the numeric gaps are because it
# only includes the WMO codes that their API is set up to return.
# Last checked for updates: 2023-01-27
WEATHERCODE_MAP = {
    0:  'Clear sky',
    1:  'Mostly clear',
    2:  'Partly cloudy',
    3:  'Overcast',
    45: 'Fog',
    48: 'Depositing rime fog',
    51: 'Light drizzle',
    53: 'Moderate drizzle',
    55: 'Dense drizzle',
    56: 'Light freezing drizzle',
    57: 'Dense freezing drizzle',
    61: 'Light rain',
    63: 'Moderate rain',
    65: 'Heavy rain',
    66: 'Light freezing rain',
    67: 'Heavy freezing rain',
    71: 'Light snow',
    73: 'Moderate snow',
    75: 'Heavy snow',
    77: 'Snow grains',
    80: 'Light showers',
    81: 'Moderate showers',
    82: 'Violent showers',
    85: 'Light snow showers',
    86: 'Heavy snow showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm, light hail',
    99: 'Thunderstorm, heavy hail',
}


def openmeteo_forecast(bot, latitude, longitude, location):
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'daily': 'temperature_2m_min,temperature_2m_max,weathercode',
        'timeformat': 'unixtime',
        'timezone': 'auto',
    }

    try:
        r = requests.get(API_ENDPOINT, params=params)
    except:
        raise Exception("An Error Occurred. Check Logs For More Information.")

    data = r.json()
    if r.status_code != 200 or data.get('error') == 'true':
        raise Exception('Error: {}'.format(data['reason']))

    weather_data = {'location': location, 'data': []}
    data = data['daily']
    for day in range(4):
        condition = data['weathercode'][day]
        condition = WEATHERCODE_MAP.get(condition, 'WMO code {}'.format(condition))

        weather_data['data'].append({
            'dow': datetime.fromtimestamp(data['time'][day]).strftime('%A'),
            'summary': condition,
            'high_temp': data['temperature_2m_max'][day],
            'low_temp': data['temperature_2m_min'][day],
        })

    return weather_data


def openmeteo_weather(bot, latitude, longitude, location):
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': 'temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m',
        'wind_speed_unit': 'ms',
        'daily': 'sunrise,sunset',
        'forecast_days': 1,
        'timeformat': 'unixtime',
        'timezone': 'auto',
    }

    try:
        r = requests.get(API_ENDPOINT, params=params)
    except:
        raise Exception("An Error Occurred. Check Logs For More Information.")

    data = r.json()
    if r.status_code != 200 or data.get('error') == 'true':
        raise Exception('Error: {}'.format(data['reason']))

    condition = data['current']['weather_code']
    condition = WEATHERCODE_MAP.get(condition, 'WMO code {}'.format(condition))

    weather_data = {
        'location': location,
        'temp': data['current']['temperature_2m'],
        'condition': condition,
        'humidity': data['current']['relative_humidity_2m'] / 100.0,  # normalize to decimal percentage
        'wind': {
            'speed': data['current']['wind_speed_10m'],
            'bearing': data['current']['wind_direction_10m'],
        },
        'timezone': data['timezone'],
    }

    if bot.config.weather.sunrise_sunset:
        weather_data['sunrise'] = data['daily']['sunrise'][0]
        weather_data['sunset'] = data['daily']['sunset'][0]

    return weather_data
