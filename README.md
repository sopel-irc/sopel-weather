# sopel-weather

A weather lookup plugin for Sopel IRC bots.

> **Note:** This package was previously published as `sopel-modules.weather`.
> Please update your dependencies to use `sopel-weather` instead.

## Installation

```bash
pip install sopel-weather
```

## Quick Start

Configure the plugin using:

```bash
sopel configure --plugins
```

Or manually edit `~/.sopel/default.cfg`:

```ini
[weather]
geocoords_provider = locationiq_us
geocoords_api_key = YOUR_LOCATIONIQ_API_KEY
weather_provider = openmeteo
weather_api_key = dummy
```

## Weather Providers

| Provider | API Key Required | Free Tier | UV Index | Features |
|----------|-----------------|-----------|----------|----------|
| **Open-Meteo** | No (use "dummy") | Unlimited | No | Best for basic weather, no signup needed |
| **Tomorrow.io** | Yes | 500 calls/day | Yes | Modern API, good accuracy |
| **Pirate Weather** | Yes | 20,000 calls/month | Yes | Dark Sky replacement |
| **OpenWeatherMap** | Yes | 1,000 calls/day | Yes | Popular, well-documented |

### Open-Meteo (Recommended for simplicity)

No API key required. Use any string (e.g., "dummy") for the weather_api_key.

```ini
[weather]
weather_provider = openmeteo
weather_api_key = dummy
```

- Website: https://open-meteo.com/
- Free for non-commercial use
- No signup required

### Tomorrow.io

Sign up at https://www.tomorrow.io/ for a free API key.

```ini
[weather]
weather_provider = tomorrow
weather_api_key = YOUR_TOMORROW_API_KEY
```

- Free tier: 500 API calls/day
- Includes UV index
- Modern REST API

### Pirate Weather

Sign up at https://pirateweather.net/ for a free API key.

```ini
[weather]
weather_provider = pirateweather
weather_api_key = YOUR_PIRATEWEATHER_API_KEY
```

- Free tier: 20,000 API calls/month
- Drop-in Dark Sky API replacement
- Includes UV index

### OpenWeatherMap

Sign up at https://openweathermap.org/ for a free API key.

```ini
[weather]
weather_provider = openweathermap
weather_api_key = YOUR_OPENWEATHERMAP_API_KEY
```

- Free tier: 1,000 API calls/day
- Includes UV index

## Geocoding Provider

A geocoding provider is required to convert location names (like "Seattle" or "90210") to coordinates.

### LocationIQ (Required)

Sign up at https://locationiq.com/ for a free API key.

```ini
[weather]
geocoords_provider = locationiq_us
geocoords_api_key = YOUR_LOCATIONIQ_API_KEY
```

Options:
- `locationiq_us` - US-based servers (recommended for North America)
- `locationiq_eu` - EU-based servers (recommended for Europe)

Free tier: 5,000 requests/day

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `geocoords_provider` | Geocoding provider (`locationiq_us`, `locationiq_eu`) | `locationiq_us` |
| `geocoords_api_key` | API key for geocoding provider | Required |
| `weather_provider` | Weather provider (`openmeteo`, `tomorrow`, `pirateweather`, `openweathermap`) | Required |
| `weather_api_key` | API key for weather provider | Required |
| `sunrise_sunset` | Show sunrise/sunset times | `False` |
| `nick_lookup` | Allow looking up weather by IRC nickname | `True` |

### Example Configuration

```ini
[weather]
geocoords_provider = locationiq_us
geocoords_api_key = pk.abc123...
weather_provider = tomorrow
weather_api_key = abc123xyz...
sunrise_sunset = True
nick_lookup = True
```

## Commands

### Current Weather

```
.weather              # Uses your saved location
.weather seattle
.weather Seattle, US
.weather 90210
```

Example output:
```
Seattle, Washington, US: 12°C (54°F), Partly Cloudy, Humidity: 75%, UV Index: 2, Gentle breeze: 19km/h (12mph) (↑)
```

### Forecast

```
.forecast             # Uses your saved location
.forecast seattle
.forecast London, UK
```

Example output:
```
Seattle, WA, US :: Monday - Partly Cloudy - 12°C (54°F) / 5°C (41°F) :: Tuesday - Rain - 14°C (57°F) / 6°C (43°F) ...
```

### Set Your Location

```
.setlocation seattle
.setlocation 98101
.setlocation London, UK
```

## Troubleshooting

### "Weather API key missing"
Set `weather_api_key` in your configuration. For Open-Meteo, use any string like "dummy".

### "GeoCoords API key missing"
Sign up at https://locationiq.com/ and add your API key to `geocoords_api_key`.

### "Could not geocode location"
- Check your LocationIQ API key is valid
- Try a more specific location (e.g., "Seattle, WA" instead of "Seattle")
- Check LocationIQ rate limits (5,000/day on free tier)

### "Error: Invalid API key"
Verify your weather provider API key is correct and active.

### UV Index not showing
UV Index is only available with Tomorrow.io, Pirate Weather, and OpenWeatherMap providers.

## Requirements

- Sopel 8.0+
- Python 3.8+

## License

MIT License
