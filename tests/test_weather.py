# coding=utf-8
"""Tests for sopel-weather"""
from __future__ import unicode_literals, absolute_import, print_function, division

import pytest
import requests_mock

import sopel_weather as weather
from sopel_weather.providers.weather.openmeteo import openmeteo_forecast, openmeteo_weather
from sopel_weather.providers.weather.pirateweather import pirateweather_forecast, pirateweather_weather
from sopel_weather.providers.weather.tomorrow import tomorrow_forecast, tomorrow_weather


# =============================================================================
# Helper Functions Tests
# =============================================================================

def test_get_temp():
    """Test temperature formatting."""
    assert weather.get_temp('') == 'unknown'
    assert weather.get_temp(None) == 'unknown'
    assert weather.get_temp(0) == '0°C (32°F)'
    assert weather.get_temp(20) == '20°C (68°F)'
    assert weather.get_temp(-10) == '-10°C (14°F)'


def test_get_humidity():
    """Test humidity formatting."""
    assert weather.get_humidity('') == 'unknown'
    assert weather.get_humidity(None) == 'unknown'
    assert weather.get_humidity(0.5) == 'Humidity: 50%'
    assert weather.get_humidity(1.0) == 'Humidity: 100%'
    assert weather.get_humidity(0.75) == 'Humidity: 75%'


def test_get_wind():
    """Test wind formatting."""
    # Test wind descriptions at different speeds (using Beaufort scale in knots)
    # The get_wind function converts m/s to knots internally
    assert 'Calm' in weather.get_wind(0.1, 0)      # < 1 knot
    assert 'Light air' in weather.get_wind(1.0, 45)    # 1-3 knots
    assert 'Light breeze' in weather.get_wind(2.5, 90)  # 4-6 knots
    assert 'Gentle breeze' in weather.get_wind(4.0, 135)  # 7-10 knots
    assert 'Moderate breeze' in weather.get_wind(6.5, 180)  # 11-15 knots
    assert 'Fresh breeze' in weather.get_wind(9.5, 225)  # 16-21 knots
    assert 'Strong breeze' in weather.get_wind(12.5, 270)  # 22-27 knots
    assert 'Near gale' in weather.get_wind(16.0, 315)  # 28-33 knots
    assert 'Gale' in weather.get_wind(19.5, 0)  # 34-40 knots
    assert 'Strong gale' in weather.get_wind(23.0, 45)  # 41-47 knots
    assert 'Storm' in weather.get_wind(27.0, 90)  # 48-55 knots
    assert 'Violent storm' in weather.get_wind(31.0, 135)  # 56-63 knots
    assert 'Hurricane' in weather.get_wind(35.0, 180)  # 64+ knots

    # Test wind direction arrows
    assert '↓' in weather.get_wind(5.0, 0)      # North wind
    assert '↙' in weather.get_wind(5.0, 45)    # NE wind
    assert '←' in weather.get_wind(5.0, 90)    # East wind
    assert '↖' in weather.get_wind(5.0, 135)   # SE wind
    assert '↑' in weather.get_wind(5.0, 180)   # South wind
    assert '↗' in weather.get_wind(5.0, 225)   # SW wind
    assert '→' in weather.get_wind(5.0, 270)   # West wind
    assert '↘' in weather.get_wind(5.0, 315)   # NW wind


# =============================================================================
# Mock Bot for Provider Tests
# =============================================================================

class MockBot:
    """Mock bot for testing providers."""
    class Config:
        class Weather:
            weather_api_key = 'test-api-key'
            sunrise_sunset = False
        weather = Weather()
    config = Config()


class MockBotWithSunrise:
    """Mock bot with sunrise_sunset enabled."""
    class Config:
        class Weather:
            weather_api_key = 'test-api-key'
            sunrise_sunset = True
        weather = Weather()
    config = Config()


# =============================================================================
# Open-Meteo Provider Tests
# =============================================================================

def test_openmeteo_weather():
    """Test Open-Meteo weather provider."""
    mock_response = {
        "latitude": 47.6,
        "longitude": -122.33,
        "timezone": "America/Los_Angeles",
        "current": {
            "temperature_2m": 12.5,
            "relative_humidity_2m": 75,
            "precipitation": 0,
            "weather_code": 2,
            "wind_speed_10m": 5.2,
            "wind_direction_10m": 180
        },
        "daily": {
            "sunrise": [1704722400],
            "sunset": [1704756000]
        }
    }

    with requests_mock.mock() as m:
        m.get('https://api.open-meteo.com/v1/forecast', json=mock_response)
        result = openmeteo_weather(MockBot(), '47.6', '-122.33', 'Seattle, WA, US')

        assert result['location'] == 'Seattle, WA, US'
        assert result['temp'] == 12.5
        assert result['condition'] == 'Partly cloudy'
        assert result['humidity'] == 0.75
        assert result['wind']['speed'] == 5.2
        assert result['wind']['bearing'] == 180
        assert result['timezone'] == 'America/Los_Angeles'


def test_openmeteo_forecast():
    """Test Open-Meteo forecast provider."""
    mock_response = {
        "latitude": 47.6,
        "longitude": -122.33,
        "timezone": "America/Los_Angeles",
        "daily": {
            "time": [1704672000, 1704758400, 1704844800, 1704931200],
            "temperature_2m_min": [5.0, 6.0, 4.5, 7.0],
            "temperature_2m_max": [12.0, 14.0, 11.5, 15.0],
            "weathercode": [2, 61, 3, 0]
        }
    }

    with requests_mock.mock() as m:
        m.get('https://api.open-meteo.com/v1/forecast', json=mock_response)
        result = openmeteo_forecast(MockBot(), '47.6', '-122.33', 'Seattle, WA, US')

        assert result['location'] == 'Seattle, WA, US'
        assert len(result['data']) == 4
        assert result['data'][0]['summary'] == 'Partly cloudy'
        assert result['data'][0]['high_temp'] == 12.0
        assert result['data'][0]['low_temp'] == 5.0
        assert result['data'][1]['summary'] == 'Light rain'


def test_openmeteo_error():
    """Test Open-Meteo error handling."""
    mock_response = {
        "error": "true",
        "reason": "Invalid coordinates"
    }

    with requests_mock.mock() as m:
        m.get('https://api.open-meteo.com/v1/forecast', json=mock_response, status_code=400)

        with pytest.raises(Exception) as exc_info:
            openmeteo_weather(MockBot(), '999', '999', 'Invalid')
        assert 'Invalid coordinates' in str(exc_info.value)


# =============================================================================
# Pirate Weather Provider Tests
# =============================================================================

def test_pirateweather_weather():
    """Test Pirate Weather provider."""
    mock_response = {
        "timezone": "America/Los_Angeles",
        "currently": {
            "temperature": 15.0,
            "summary": "Partly Cloudy",
            "humidity": 0.65,
            "windSpeed": 4.5,
            "windBearing": 270,
            "uvIndex": 3
        },
        "daily": {
            "data": [{
                "sunriseTime": 1704722400,
                "sunsetTime": 1704756000
            }]
        }
    }

    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, json=mock_response)
        result = pirateweather_weather(MockBot(), '47.6', '-122.33', 'Seattle, WA, US')

        assert result['location'] == 'Seattle, WA, US'
        assert result['temp'] == 15.0
        assert result['condition'] == 'Partly Cloudy'
        assert result['humidity'] == 0.65
        assert result['wind']['speed'] == 4.5
        assert result['wind']['bearing'] == 270
        assert result['uvindex'] == 3
        assert result['timezone'] == 'America/Los_Angeles'


def test_pirateweather_forecast():
    """Test Pirate Weather forecast provider."""
    mock_response = {
        "timezone": "America/Los_Angeles",
        "daily": {
            "data": [
                {"time": 1704672000, "summary": "Partly cloudy.", "temperatureHigh": 12.0, "temperatureLow": 5.0},
                {"time": 1704758400, "summary": "Rain.", "temperatureHigh": 14.0, "temperatureLow": 6.0},
                {"time": 1704844800, "summary": "Overcast.", "temperatureHigh": 11.5, "temperatureLow": 4.5},
                {"time": 1704931200, "summary": "Clear.", "temperatureHigh": 15.0, "temperatureLow": 7.0},
            ]
        }
    }

    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, json=mock_response)
        result = pirateweather_forecast(MockBot(), '47.6', '-122.33', 'Seattle, WA, US')

        assert result['location'] == 'Seattle, WA, US'
        assert len(result['data']) == 4
        assert result['data'][0]['summary'] == 'Partly cloudy'
        assert result['data'][0]['high_temp'] == 12.0
        assert result['data'][0]['low_temp'] == 5.0
        assert result['data'][1]['summary'] == 'Rain'


def test_pirateweather_error():
    """Test Pirate Weather error handling."""
    mock_response = {"error": "Invalid API key"}

    with requests_mock.mock() as m:
        m.get(requests_mock.ANY, json=mock_response, status_code=401)

        with pytest.raises(Exception) as exc_info:
            pirateweather_weather(MockBot(), '47.6', '-122.33', 'Seattle, WA, US')
        assert 'Invalid API key' in str(exc_info.value)


# =============================================================================
# Tomorrow.io Provider Tests
# =============================================================================

def test_tomorrow_weather():
    """Test Tomorrow.io weather provider."""
    mock_response = {
        "location": {
            "lat": 47.6,
            "lon": -122.33,
            "timezone": "America/Los_Angeles"
        },
        "timelines": {
            "minutely": [{
                "time": "2024-01-08T12:00:00Z",
                "values": {
                    "temperature": 12.5,
                    "humidity": 75,
                    "windSpeed": 5.2,
                    "windDirection": 180,
                    "weatherCode": 1101,
                    "uvIndex": 2
                }
            }],
            "daily": [{
                "time": "2024-01-08T00:00:00Z",
                "values": {
                    "sunriseTime": "2024-01-08T07:30:00Z",
                    "sunsetTime": "2024-01-08T16:45:00Z",
                    "temperatureMax": 15.0,
                    "temperatureMin": 8.0,
                    "weatherCodeMax": 1101
                }
            }]
        }
    }

    with requests_mock.mock() as m:
        m.get('https://api.tomorrow.io/v4/weather/forecast', json=mock_response)
        result = tomorrow_weather(MockBot(), '47.6', '-122.33', 'Seattle, WA, US')

        assert result['location'] == 'Seattle, WA, US'
        assert result['temp'] == 12.5
        assert result['condition'] == 'Partly Cloudy'
        assert result['humidity'] == 0.75
        assert result['wind']['speed'] == 5.2
        assert result['wind']['bearing'] == 180
        assert result['uvindex'] == 2
        assert result['timezone'] == 'America/Los_Angeles'


def test_tomorrow_weather_with_sunrise():
    """Test Tomorrow.io weather provider with sunrise/sunset enabled."""
    mock_response = {
        "location": {
            "lat": 47.6,
            "lon": -122.33,
            "timezone": "America/Los_Angeles"
        },
        "timelines": {
            "minutely": [{
                "time": "2024-01-08T12:00:00Z",
                "values": {
                    "temperature": 12.5,
                    "humidity": 75,
                    "windSpeed": 5.2,
                    "windDirection": 180,
                    "weatherCode": 1101,
                    "uvIndex": 2
                }
            }],
            "daily": [{
                "time": "2024-01-08T00:00:00Z",
                "values": {
                    "sunriseTime": "2024-01-08T07:30:00Z",
                    "sunsetTime": "2024-01-08T16:45:00Z",
                    "temperatureMax": 15.0,
                    "temperatureMin": 8.0,
                    "weatherCodeMax": 1101
                }
            }]
        }
    }

    with requests_mock.mock() as m:
        m.get('https://api.tomorrow.io/v4/weather/forecast', json=mock_response)
        result = tomorrow_weather(MockBotWithSunrise(), '47.6', '-122.33', 'Seattle, WA, US')

        assert 'sunrise' in result
        assert 'sunset' in result
        assert isinstance(result['sunrise'], int)
        assert isinstance(result['sunset'], int)


def test_tomorrow_forecast():
    """Test Tomorrow.io forecast provider."""
    mock_response = {
        "location": {
            "lat": 47.6,
            "lon": -122.33,
            "timezone": "America/Los_Angeles"
        },
        "timelines": {
            "daily": [
                {
                    "time": "2024-01-08T00:00:00Z",
                    "values": {
                        "temperatureMax": 12.0,
                        "temperatureMin": 5.0,
                        "weatherCodeMax": 1101
                    }
                },
                {
                    "time": "2024-01-09T00:00:00Z",
                    "values": {
                        "temperatureMax": 14.0,
                        "temperatureMin": 6.0,
                        "weatherCodeMax": 4001
                    }
                },
                {
                    "time": "2024-01-10T00:00:00Z",
                    "values": {
                        "temperatureMax": 11.5,
                        "temperatureMin": 4.5,
                        "weatherCodeMax": 1001
                    }
                },
                {
                    "time": "2024-01-11T00:00:00Z",
                    "values": {
                        "temperatureMax": 15.0,
                        "temperatureMin": 7.0,
                        "weatherCodeMax": 1000
                    }
                }
            ]
        }
    }

    with requests_mock.mock() as m:
        m.get('https://api.tomorrow.io/v4/weather/forecast', json=mock_response)
        result = tomorrow_forecast(MockBot(), '47.6', '-122.33', 'Seattle, WA, US')

        assert result['location'] == 'Seattle, WA, US'
        assert len(result['data']) == 4
        assert result['data'][0]['summary'] == 'Partly Cloudy'
        assert result['data'][0]['high_temp'] == 12.0
        assert result['data'][0]['low_temp'] == 5.0
        assert result['data'][1]['summary'] == 'Rain'
        assert result['data'][2]['summary'] == 'Cloudy'
        assert result['data'][3]['summary'] == 'Clear'


def test_tomorrow_error():
    """Test Tomorrow.io error handling."""
    mock_response = {"message": "Invalid API key"}

    with requests_mock.mock() as m:
        m.get('https://api.tomorrow.io/v4/weather/forecast', json=mock_response, status_code=401)

        with pytest.raises(Exception) as exc_info:
            tomorrow_weather(MockBot(), '47.6', '-122.33', 'Seattle, WA, US')
        assert 'Invalid API key' in str(exc_info.value)


def test_tomorrow_weather_codes():
    """Test Tomorrow.io weather code mapping."""
    from sopel_weather.providers.weather.tomorrow import WEATHER_CODES

    assert WEATHER_CODES[1000] == 'Clear'
    assert WEATHER_CODES[1001] == 'Cloudy'
    assert WEATHER_CODES[1101] == 'Partly Cloudy'
    assert WEATHER_CODES[4001] == 'Rain'
    assert WEATHER_CODES[5000] == 'Snow'
    assert WEATHER_CODES[8000] == 'Thunderstorm'
    assert WEATHER_CODES[2000] == 'Fog'
    assert WEATHER_CODES[6001] == 'Freezing Rain'
    assert WEATHER_CODES[7000] == 'Ice Pellets'
