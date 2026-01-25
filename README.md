# sopel-weather

A weather lookup plugin for Sopel IRC bots.

> **Note:** This package was previously published as `sopel-modules.weather`.
> Please update your dependencies to use `sopel-weather` instead.

## Installation

```bash
pip install sopel-weather
```

## Configuration

You can automatically configure this plugin using `sopel configure --plugins`.

Or configure manually in `~/.sopel/default.cfg`:

```ini
[weather]
geocoords_provider = locationiq_us
geocoords_api_key = YOUR_LOCATIONIQ_API_KEY
weather_provider = openmeteo
weather_api_key = dummy
```

## Usage

### Current Weather

```
.weather              # Uses your saved location
.weather seattle, us
.weather london
```

Example output:
```
Paris, Ile-de-France, FR: 6°C (42°F), Clear, Humidity: 83%, UV Index: 0, Gentle breeze 4.0m/s (↗)
```

### Forecast

```
.forecast              # Uses your saved location
.forecast seattle, us
.forecast london
```

### Set Your Location

```
.setlocation london    # Set by city name
.setlocation 98101     # Set by US zip code
```

## API Keys Required

### GeoCoords Provider
- [LocationIQ](https://locationiq.com/) - Free tier available

### Weather Providers

- **Open-Meteo** - No API key required (use any string)
  - https://open-meteo.com/
- **OpenWeatherMap** - Free tier available
  - https://openweathermap.org/
- **Pirate Weather** - Drop-in Dark Sky replacement
  - https://pirateweather.net/

## Requirements

- Sopel 8.0+
- Python 3.8+

## License

MIT License
