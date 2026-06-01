# Weather API Replacement Research — DarkSky Migration

## Context

The stargazr2_BE API used DarkSky for weather data. DarkSky was shut down (acquired by Apple).
The app only consumed 5 fields from DarkSky:

- `currently.precipProbability` — probability of precipitation (0–1)
- `currently.humidity` — relative humidity (0–1)
- `currently.cloudCover` — cloud cover fraction (0–1)
- `currently.visibility` — visibility distance (not currently used in rating)
- `daily.data[0].moonPhase` — fractional lunar phase (0–1)

Requests are point-based (exact lat/lon), for either current/future (up to 8 days out)
or recent past (up to 1 day back), passed as a Unix timestamp.

---

## Candidates Evaluated

| | **Pirate Weather** | **Open-Meteo** | **WeatherAPI.com** | **Visual Crossing** |
|---|---|---|---|---|
| **Free limit** | ~666/day (20K/mo) | **10,000/day** | ~3,333/day (100K/mo) | 1,000/day* |
| **API key required** | Yes | No | Yes | Yes |
| **Grid-interpolated (not nearest-station)** | Yes (NOAA NWP) | **Yes (best resolution)** | Partial | Yes (blended models) |
| **Historical data** | Yes (timemachine endpoint) | Yes (back to 1940) | Yes (back to 2010) | Yes (back to 1970) |
| **Forecast range** | 7 days | 16 days | 14 days | 15 days |
| **precipProbability** | Yes | Yes | Yes | Yes |
| **humidity** | Yes | Yes | Yes | Yes |
| **cloudCover** | Yes | Yes | Yes | Yes |
| **visibility** | Yes | Yes | Yes | Yes |
| **moonPhase** | Yes (native) | No (calculated locally) | No (calculated locally) | Yes (native) |
| **DarkSky drop-in** | **Yes (identical format)** | No | No | No |
| **Already in codebase** | No | No | No | Yes (partial, unwired) |
| **Vendor risk** | Low (open-source) | **Lowest (open-source)** | Medium (dropped free plan once in 2022) | Low |

*Visual Crossing counts per "record" not per call — one call for a single hour = ~1 record.
For the app's single-hour lookup pattern, the 1,000/day limit effectively behaves as 1,000 calls/day.

---

## Option Notes

### Pirate Weather
- Purpose-built DarkSky clone — identical URL structure and JSON schema
- Would require near-zero code changes (swap base URL + env var)
- Uses NOAA HRRR/GFS/NBM ensemble; better coverage for North America than globally
- Free tier: 20,000 calls/month (~666/day) — below 1,000/day threshold but above 100/day

### Open-Meteo ← CHOSEN
- Open-source, non-commercial use is free with no API key
- Uses high-resolution NWP grid models (ERA5, HRRR, GFS, etc.) — true interpolated point data
- `past_days=2` + `forecast_days=16` with `start_hour`/`end_hour` covers the full app range
  in a single endpoint (`/v1/forecast`)
- Moon phase not provided — calculated locally using synodic period math (no extra dependency)
- All needed weather fields available in hourly resolution
- Note: Open-Meteo returns percentages (0–100); must divide by 100 to match prior 0–1 fractions

### WeatherAPI.com
- Most generous free tier (~3,333/day)
- Generous but commercial — free plan was previously dropped (2022) and reinstated
- Different response format; significant refactor required

### Visual Crossing
- Already partially integrated in apis.py (VISUAL_CROSSING_URL defined, key hardcoded)
- Returns moonphase natively (same 0–1 scale as DarkSky)
- 1,000 records/day free; paid tier is $0.0001/record beyond that
- Different response format from DarkSky; moderate refactor required

---

## Decision: Open-Meteo

Chosen for: highest free limit (10K/day), no API key, open-source/no vendor risk,
true grid-interpolated point forecasts, covers all required fields, single endpoint
handles both historical and forecast queries.

Moon phase is calculated locally — see `_calculate_moon_phase()` in main.py.
Reference point: new moon at 2000-01-06 18:14 UTC (Unix: 947182440), synodic period 29.53058867 days.
