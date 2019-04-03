# coding=utf-8
"""Tests for message formatting"""
from __future__ import unicode_literals, absolute_import, print_function, division

import pytest
import requests_mock
import sopel.tools.target

from sopel.trigger import PreTrigger, Trigger
from sopel.test_tools import MockSopel, MockSopelWrapper
from sopel.tools import Identifier
from sopel import module

from sopel_modules.weather import weather


@pytest.fixture
def sopel():
    bot = MockSopel('Sopel')
    bot.config.core.owner = 'Bar'
    return bot


@pytest.fixture
def bot(sopel, pretrigger):
    bot = MockSopelWrapper(sopel, pretrigger)
    bot.privileges = dict()
    bot.privileges[Identifier('#Sopel')] = dict()
    bot.privileges[Identifier('#Sopel')][Identifier('Foo')] = module.VOICE
    return bot


@pytest.fixture
def pretrigger():
    line = ':Foo!foo@example.com PRIVMSG #sopel :.weather 90210'
    return PreTrigger(Identifier('Foo'), line)


@pytest.fixture
def trigger(bot, pretrigger):
    return Trigger(bot.config, pretrigger, None)


@pytest.fixture
def weather_results():
    with requests_mock.mock() as m:
        m.get('https://api.openweathermap.org/data/2.5/weather?id=5400075&appid=123456&units=metric',
              json={"coord": {"lon": -122.04, "lat": 37.37},
                    "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01n"}],
                    "base": "stations",
                    "main": {"temp": 55.17, "pressure": 1014, "humidity": 79, "temp_min": 55.04,
                             "temp_max": 55.4}, "visibility": 16093,
                    "wind": {"speed": 11.41, "deg": 260, "gust": 8.2}, "clouds": {"all": 1}, "dt": 1546848000,
                    "sys": {"type": 1, "id": 5122, "message": 0.0191, "country": "US", "sunrise": 1546874568,
                            "sunset": 1546909596}, "id": 5400075, "name": "Sunnyvale", "cod": 200},
              status_code=200)
        return weather.search('weather', 'w5400075', '123456')


@pytest.fixture
def weather_results_utf8():
    with requests_mock.mock() as m:
        m.get('https://api.openweathermap.org/data/2.5/weather?id=655977&appid=123456&units=metric',
              json={"coord": {"lon": 25.08, "lat": 60.47},
                    "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
                    "base": "stations",
                    "main": {"temp": 10.85, "pressure": 1022, "humidity": 29, "temp_min": 10.56, "temp_max": 11.67},
                    "visibility": 10000, "wind": {"speed": 6.7, "deg": 160}, "clouds": {"all": 0}, "dt": 1554295687,
                    "sys": {"type": 1, "id": 1332, "message": 0.0038, "country": "FI", "sunrise": 1554262754,
                            "sunset": 1554311195}, "id": 655977, "name": "Järvenpää", "cod": 200},
              status_code=200)
        return weather.search('weather', 'w655977', '123456')


@pytest.fixture
def forecast_results():
    with requests_mock.mock() as m:
        m.get('https://api.openweathermap.org/data/2.5/forecast?id=2643743&appid=123456&units=metric',
              json={"list": [{"dt": 1546862400,
                              "main": {"temp": 11.27, "temp_min": 6.04, "temp_max": 11.27},
                              "weather": [{"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02d"}],
                              "dt_txt": "2019-01-07 12:00:00"},
                             {"dt": 1546873200,
                              "main": {"temp": 11.87, "temp_min": 7.95, "temp_max": 11.87},
                              "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}],
                              "dt_txt": "2019-01-07 15:00:00"},
                             {"dt": 1546884000,
                              "main": {"temp": 10.19, "temp_min": 7.58, "temp_max": 10.19},
                              "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10n"}],
                              "dt_txt": "2019-01-07 18:00:00"},
                             {"dt": 1546894800,
                              "main": {"temp": 9.24, "temp_min": 7.93, "temp_max": 9.24},
                              "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10n"}],
                              "dt_txt": "2019-01-07 21:00:00"},
                             {"dt": 1546905600,
                              "main": {"temp": 7.46, "temp_min": 7.46, "temp_max": 7.46},
                              "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10n"}],
                              "dt_txt": "2019-01-08 00:00:00"},
                             {"dt": 1546916400,
                              "main": {"temp": 5.29, "temp_min": 5.29, "temp_max": 5.29},
                              "weather": [
                                  {"id": 802, "main": "Clouds", "description": "scattered clouds", "icon": "03n"}],
                              "dt_txt": "2019-01-08 03:00:00"},
                             {"dt": 1546927200,
                              "main": {"temp": 5.71, "temp_min": 5.71, "temp_max": 5.71},
                              "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10n"}],
                              "dt_txt": "2019-01-08 06:00:00"},
                             {"dt": 1546938000,
                              "main": {"temp": 6.07, "temp_min": 6.07, "temp_max": 6.07},
                              "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}],
                              "dt_txt": "2019-01-08 09:00:00"},
                             {"dt": 1546948800,
                              "main": {"temp": 7.23, "temp_min": 7.23, "temp_max": 7.23},
                              "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
                              "dt_txt": "2019-01-08 12:00:00"},
                             {"dt": 1546959600,
                              "main": {"temp": 6.71, "temp_min": 6.71, "temp_max": 6.71},
                              "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
                              "dt_txt": "2019-01-08 15:00:00"}],
                    "city": {"id": 2643743, "name": "London", "coord": {"lat": 51.5073, "lon": -0.1277},
                             "country": "GB",
                             "population": 1000000}},
              status_code=200)
        return weather.search('forecast', 'w2643743', '123456')


def test_forecast_command(bot, trigger):
    @module.commands('forecast')
    @module.example('.forecast', 'True')
    def mock(bot, trigger, match=None):
        return True

    assert mock(bot, trigger) is True


def test_wea_command(bot, trigger):
    @module.commands('wea')
    @module.example('.wea', 'True')
    def mock(bot, trigger, match=None):
        return True

    assert mock(bot, trigger) is True


def test_weather_command(bot, trigger):
    @module.commands('weather')
    @module.example('.weather', 'True')
    def mock(bot, trigger, match=None):
        return True

    assert mock(bot, trigger) is True


def test_setup(bot, trigger):
    weather.setup(bot)
    assert bot.config.weather is not None


# TODO - Determine how to test .configure()
'''
def test_configure(bot, trigger):
    weather.configure(bot.config)
    assert bot.config.weather
'''


def test_location_search():
    with requests_mock.mock() as m:
        m.get('https://api.openweathermap.org/data/2.5/weather?q=Seattle&appid=123456&units=metric',
              json={"coord": {"lon": -122.33, "lat": 47.6},
                    "weather": [{"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02n"}],
                    "base": "stations",
                    "main": {"temp": 7.76, "pressure": 1010, "humidity": 79, "temp_min": 6.7,
                             "temp_max": 8.3}, "visibility": 16093,
                    "wind": {"speed": 1.41, "deg": 68.0002}, "clouds": {"all": 20}, "dt": 1546663980,
                    "sys": {"type": 1, "id": 3417, "message": 0.0071, "country": "US",
                            "sunrise": 1546703824, "sunset": 1546734771}, "id": 5809844,
                    "name": "Seattle", "cod": 200},
              status_code=200)
        result = weather.search('weather', 'Seattle', '123456')
        assert result['id'] == 5809844
        assert result['name'] == 'Seattle'
        assert result['wind']['deg'] == 68.0002
        assert result['wind']['speed'] == 1.41


def test_woeid_search():
    with requests_mock.mock() as m:
        m.get('https://api.openweathermap.org/data/2.5/weather?id=5400075&appid=123456&units=metric',
              json={"coord": {"lon": -122.04, "lat": 37.37},
                    "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01n"}],
                    "base": "stations",
                    "main": {"temp": 55.17, "pressure": 1014, "humidity": 79, "temp_min": 55.04,
                             "temp_max": 55.4}, "visibility": 16093,
                    "wind": {"speed": 11.41, "deg": 260, "gust": 8.2}, "clouds": {"all": 1}, "dt": 1546848000,
                    "sys": {"type": 1, "id": 5122, "message": 0.0191, "country": "US", "sunrise": 1546874568,
                            "sunset": 1546909596}, "id": 5400075, "name": "Sunnyvale", "cod": 200},
              status_code=200)
        result = weather.search('weather', 'w5400075', '123456')
        assert result['id'] == 5400075
        assert result['name'] == 'Sunnyvale'
        assert result['wind']['deg'] == 260
        assert result['wind']['speed'] == 11.41


def test_zip_search():
    with requests_mock.mock() as m:
        m.get('https://api.openweathermap.org/data/2.5/weather?zip=90210&appid=123456&units=metric',
              json={"coord": {"lon": -118.4, "lat": 34.07},
                    "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10n"}],
                    "base": "stations",
                    "main": {"temp": 54.05, "pressure": 1023, "humidity": 96, "temp_min": 50,
                             "temp_max": 55.94}, "visibility": 12874, "wind": {"speed": 9.17, "deg": 110},
                    "rain": {"1h": 0.76}, "clouds": {"all": 90}, "dt": 1546847580,
                    "sys": {"type": 1, "id": 3514, "message": 0.0095, "country": "US", "sunrise": 1546873193,
                            "sunset": 1546909223}, "id": 420004549, "name": "Beverly Hills", "cod": 200},
              status_code=200)
        result = weather.search('weather', '90210', '123456')
        assert result['id'] == 420004549
        assert result['name'] == 'Beverly Hills'
        assert result['wind']['deg'] == 110
        assert result['wind']['speed'] == 9.17


def test_search_none():
    with requests_mock.mock() as m:
        m.get('https://api.openweathermap.org/data/2.5/weather?q=Seattle&appid=123456&units=metric',
              json={},
              status_code=200)
        result = weather.search('weather', 'Seattle', '123456')
        assert result == {}


def test_search_401():
    with requests_mock.mock() as m:
        m.get('https://api.openweathermap.org/data/2.5/weather?q=Seattle&appid=123456&units=metric',
              json={},
              status_code=401)
        result = weather.search('weather', 'Seattle', '123456')
        assert result is None


def test_get_condition(weather_results):
    condition = weather.get_condition('')
    assert condition == 'unknown'
    condition = weather.get_condition(weather_results)
    assert condition == 'Clear'


def test_get_temp(weather_results):
    temp = weather.get_temp('')
    assert temp == 'unknown'
    temp = weather.get_temp(weather_results)
    assert temp == '55°C (131°F)'


def test_get_humidity(weather_results):
    humidity = weather.get_humidity('')
    assert humidity == 'unknown'
    humidity = weather.get_humidity(weather_results)
    assert humidity == 'Humidity: 79%'


def test_get_wind(weather_results):
    wind = weather.get_wind('')
    assert wind == 'unknown'

    wind = weather.get_wind(weather_results)
    assert wind == 'Strong breeze 11.4m/s (→)'

    weather_results['wind']['deg'] = 0
    weather_results['wind']['speed'] = 0.1
    wind = weather.get_wind(weather_results)
    assert wind == 'Calm 0.1m/s (↓)'

    weather_results['wind']['deg'] = 45
    weather_results['wind']['speed'] = 1.5
    wind = weather.get_wind(weather_results)
    assert wind == 'Light air 1.5m/s (↙)'

    weather_results['wind']['deg'] = 90
    weather_results['wind']['speed'] = 2.5
    wind = weather.get_wind(weather_results)
    assert wind == 'Light breeze 2.5m/s (←)'

    weather_results['wind']['deg'] = 135
    weather_results['wind']['speed'] = 4
    wind = weather.get_wind(weather_results)
    assert wind == 'Gentle breeze 4.0m/s (↖)'

    weather_results['wind']['deg'] = 180
    weather_results['wind']['speed'] = 6
    wind = weather.get_wind(weather_results)
    assert wind == 'Moderate breeze 6.0m/s (↑)'

    weather_results['wind']['deg'] = 225
    weather_results['wind']['speed'] = 8
    wind = weather.get_wind(weather_results)
    assert wind == 'Fresh breeze 8.0m/s (↗)'

    weather_results['wind']['deg'] = 270
    weather_results['wind']['speed'] = 12
    wind = weather.get_wind(weather_results)
    assert wind == 'Strong breeze 12.0m/s (→)'

    weather_results['wind']['deg'] = 315
    weather_results['wind']['speed'] = 16
    wind = weather.get_wind(weather_results)
    assert wind == 'Near gale 16.0m/s (↘)'

    weather_results['wind']['deg'] = 0
    weather_results['wind']['speed'] = 20
    wind = weather.get_wind(weather_results)
    assert wind == 'Gale 20.0m/s (↓)'

    weather_results['wind']['deg'] = 45
    weather_results['wind']['speed'] = 24
    wind = weather.get_wind(weather_results)
    assert wind == 'Strong gale 24.0m/s (↙)'

    weather_results['wind']['deg'] = 90
    weather_results['wind']['speed'] = 28
    wind = weather.get_wind(weather_results)
    assert wind == 'Storm 28.0m/s (←)'

    weather_results['wind']['deg'] = 135
    weather_results['wind']['speed'] = 32
    wind = weather.get_wind(weather_results)
    assert wind == 'Violent storm 32.0m/s (↖)'

    weather_results['wind']['deg'] = 180
    weather_results['wind']['speed'] = 50
    wind = weather.get_wind(weather_results)
    assert wind == 'Hurricane 50.0m/s (↑)'


def test_get_condition_utf8(weather_results_utf8):
    condition = weather.get_condition('')
    assert condition == 'unknown'
    condition = weather.get_condition(weather_results_utf8)
    assert condition == 'Clear'


def test_get_temp_utf8(weather_results_utf8):
    temp = weather.get_temp('')
    assert temp == 'unknown'
    temp = weather.get_temp(weather_results_utf8)
    assert temp == '11°C (52°F)'


def test_get_humidity_utf8(weather_results_utf8):
    humidity = weather.get_humidity('')
    assert humidity == 'unknown'
    humidity = weather.get_humidity(weather_results_utf8)
    assert humidity == 'Humidity: 29%'


# TODO - Add the remaining condition tests
def test_get_tomorrow_condition(forecast_results):
    tomorrow_condition = weather.get_tomorrow_condition(forecast_results)
    assert tomorrow_condition == 'Light Rain'


def test_get_tomorrow_high(forecast_results):
    tomorrow_high = weather.get_tomorrow_high(forecast_results)
    assert tomorrow_high == 'High: 11°C (53°F)'


def test_get_tomorrow_low(forecast_results):
    tomorrow_low = weather.get_tomorrow_low(forecast_results)
    assert tomorrow_low == 'Low: 5°C (41°F)'
