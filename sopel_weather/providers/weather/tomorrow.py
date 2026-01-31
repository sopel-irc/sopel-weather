# coding=utf-8
import requests

from datetime import datetime


API_ENDPOINT = 'https://api.tomorrow.io/v4/weather/forecast'

# Tomorrow.io weather codes
# https://docs.tomorrow.io/reference/data-layers-weather-codes
WEATHER_CODES = {
    0: "Unknown",
    1000: "Clear",
    1001: "Cloudy",
    1100: "Mostly Clear",
    1101: "Partly Cloudy",
    1102: "Mostly Cloudy",
    2000: "Fog",
    2100: "Light Fog",
    4000: "Drizzle",
    4001: "Rain",
    4200: "Light Rain",
    4201: "Heavy Rain",
    5000: "Snow",
    5001: "Flurries",
    5100: "Light Snow",
    5101: "Heavy Snow",
    6000: "Freezing Drizzle",
    6001: "Freezing Rain",
    6200: "Light Freezing Rain",
    6201: "Heavy Freezing Rain",
    7000: "Ice Pellets",
    7101: "Heavy Ice Pellets",
    7102: "Light Ice Pellets",
    8000: "Thunderstorm",
}


def tomorrow_forecast(bot, latitude, longitude, location):
    params = {
        'location': '{},{}'.format(latitude, longitude),
        'apikey': bot.config.weather.weather_api_key,
        'units': 'metric',
        'timesteps': 'daily',
    }

    try:
        r = requests.get(API_ENDPOINT, params=params)
    except:
        raise Exception("An Error Occurred. Check Logs For More Information.")

    data = r.json()
    if r.status_code != 200:
        error_msg = data.get('message', data.get('error', 'Unknown error'))
        raise Exception('Error: {}'.format(error_msg))

    weather_data = {'location': location, 'data': []}

    daily_data = data['timelines']['daily']
    for day in daily_data[:4]:
        weather_code = day['values'].get('weatherCodeMax', 0)
        condition = WEATHER_CODES.get(weather_code, 'Unknown')

        weather_data['data'].append({
            'dow': datetime.fromisoformat(day['time'].replace('Z', '+00:00')).strftime('%A'),
            'summary': condition,
            'high_temp': day['values']['temperatureMax'],
            'low_temp': day['values']['temperatureMin'],
        })

    return weather_data


def tomorrow_weather(bot, latitude, longitude, location):
    params = {
        'location': '{},{}'.format(latitude, longitude),
        'apikey': bot.config.weather.weather_api_key,
        'units': 'metric',
        'timesteps': 'current,daily',
    }

    try:
        r = requests.get(API_ENDPOINT, params=params)
    except:
        raise Exception("An Error Occurred. Check Logs For More Information.")

    data = r.json()
    if r.status_code != 200:
        error_msg = data.get('message', data.get('error', 'Unknown error'))
        raise Exception('Error: {}'.format(error_msg))

    current = data['timelines']['minutely'][0]['values']
    weather_code = current.get('weatherCode', 0)
    condition = WEATHER_CODES.get(weather_code, 'Unknown')

    # Wind speed from Tomorrow.io is in m/s when using metric units
    weather_data = {
        'location': location,
        'temp': current['temperature'],
        'condition': condition,
        'humidity': current['humidity'] / 100.0,  # normalize to decimal percentage
        'wind': {
            'speed': current['windSpeed'],
            'bearing': current['windDirection'],
        },
        'uvindex': current.get('uvIndex'),
        'timezone': data['location'].get('timezone', 'UTC'),
    }

    if bot.config.weather.sunrise_sunset:
        daily = data['timelines']['daily'][0]['values']
        # Parse ISO format timestamps and convert to Unix timestamps
        sunrise_str = daily.get('sunriseTime', '')
        sunset_str = daily.get('sunsetTime', '')
        if sunrise_str:
            weather_data['sunrise'] = int(datetime.fromisoformat(
                sunrise_str.replace('Z', '+00:00')).timestamp())
        if sunset_str:
            weather_data['sunset'] = int(datetime.fromisoformat(
                sunset_str.replace('Z', '+00:00')).timestamp())

    return weather_data
