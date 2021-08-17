from typing import Any

from freezegun import freeze_time
import mock

from dashy.sources.openweathermap.weather import Weather
import pytest

HOURS = 3600

MOCK_WEATHER = {
    "hourly": [
        {
            "dt": 12 * HOURS,
            "temp": 18,
            "humidity": 55,
            "wind_speed": 3,
            "weather": [{"description": "Slight rain"}],
            "rain": {"1h": 2},
        },
        {
            "dt": 13 * HOURS,
            "temp": 19,
            "humidity": 52,
            "wind_speed": 3,
            "weather": [{"description": "Slight rain"}],
            "rain": {"1h": 2},
        },
        {
            "dt": 14 * HOURS,
            "temp": 19,
            "humidity": 51,
            "wind_speed": 4,
            "weather": [{"description": "Cloudy"}],
        },
        {
            "dt": 15 * HOURS,
            "temp": 20,
            "humidity": 52,
            "wind_speed": 1,
            "weather": [{"description": "Sunny"}],
        },
        {
            "dt": 16 * HOURS,
            "temp": 21,
            "humidity": 52,
            "wind_speed": 1,
            "weather": [{"description": "Sunny"}],
        },
        {
            "dt": 17 * HOURS,
            "temp": 23,
            "humidity": 49,
            "wind_speed": 2,
            "weather": [{"description": "Very sunny"}],
        },
        {
            "dt": 18 * HOURS,
            "temp": 22,
            "humidity": 51,
            "wind_speed": 2,
            "weather": [{"description": "Overcast clouds"}],
            "rain": {"1h": 2},
        },
        {
            "dt": 19 * HOURS,
            "temp": 26,
            "humidity": 89,
            "wind_speed": 27,
            "weather": [{"description": "Tropical storm"}],
            "rain": {"1h": 54},
        },
    ]
}


@pytest.fixture(autouse=True)
def mock_openweathermap_env(monkeypatch: Any) -> None:
    monkeypatch.setenv("OPENWEATHERMAP_LAT", "1")
    monkeypatch.setenv("OPENWEATHERMAP_LON", "1")
    monkeypatch.setenv("OPENWEATHERMAP_API_KEY", "1")


@freeze_time("2020-01-01", tz_offset=0)
def test_weather_every_hour() -> None:
    weather = Weather(20, 45, lat="1", lon="1", api_key="", rows=10, every_hours=1)
    with mock.patch.object(weather, "_get_source", return_value=MOCK_WEATHER):
        rows = list(weather.get_lines())

    expected = [
        "Hour  Weather             Temp Hum Rain Wind ",
        "12:00 Slight Rain         18°C 55% 2mm  3m/s ",
        "13:00 Slight Rain         19°C 52% 2mm  3m/s ",
        "14:00 Cloudy              19°C 51%      4m/s ",
        "15:00 Sunny               20°C 52%      1m/s ",
        "16:00 Sunny               21°C 52%      1m/s ",
        "17:00 Very Sunny          23°C 49%      2m/s ",
        "18:00 Overcast Clouds     22°C 51% 2mm  2m/s ",
        "19:00 Tropical Storm      26°C 89% 54mm 27m/s",
    ]

    assert rows == expected


@freeze_time("2020-01-01", tz_offset=5)
def test_weather_different_timezone() -> None:
    weather = Weather(20, 45, lat="1", lon="1", api_key="", rows=10, every_hours=1)
    with mock.patch.object(weather, "_get_source", return_value=MOCK_WEATHER):
        rows = list(weather.get_lines())

    expected = [
        "Hour  Weather             Temp Hum Rain Wind ",
        "17:00 Slight Rain         18°C 55% 2mm  3m/s ",
        "18:00 Slight Rain         19°C 52% 2mm  3m/s ",
        "19:00 Cloudy              19°C 51%      4m/s ",
        "20:00 Sunny               20°C 52%      1m/s ",
        "21:00 Sunny               21°C 52%      1m/s ",
        "22:00 Very Sunny          23°C 49%      2m/s ",
        "23:00 Overcast Clouds     22°C 51% 2mm  2m/s ",
        "00:00 Tropical Storm      26°C 89% 54mm 27m/s",
    ]

    assert rows == expected


@freeze_time("2020-01-01", tz_offset=0)
def test_weather_every_other_hour() -> None:
    weather = Weather(20, 45, lat="1", lon="1", api_key="", rows=10, every_hours=2)
    with mock.patch.object(weather, "_get_source", return_value=MOCK_WEATHER):
        rows = list(weather.get_lines())

    expected = [
        "Hour  Weather             Temp Hum Rain Wind ",
        "12:00 Slight Rain         18°C 55% 2mm  3m/s ",
        "14:00 Cloudy              19°C 51%      4m/s ",
        "16:00 Sunny               21°C 52%      1m/s ",
        "18:00 Overcast Clouds     22°C 51% 2mm  2m/s ",
    ]

    assert rows == expected


@freeze_time("2020-01-01", tz_offset=0)
def test_weather_every_third_hour() -> None:
    weather = Weather(20, 45, lat="1", lon="1", api_key="", rows=10, every_hours=3)
    with mock.patch.object(weather, "_get_source", return_value=MOCK_WEATHER):
        rows = list(weather.get_lines())

    expected = [
        "Hour  Weather             Temp Hum Rain Wind ",
        "12:00 Slight Rain         18°C 55% 2mm  3m/s ",
        "15:00 Sunny               20°C 52%      1m/s ",
        "18:00 Overcast Clouds     22°C 51% 2mm  2m/s ",
    ]

    assert rows == expected


@freeze_time("2020-01-01", tz_offset=0)
def test_weather_hiding_title() -> None:
    weather = Weather(20, 40, lat="1", lon="1", api_key="", rows=10, every_hours=1)
    with mock.patch.object(weather, "_get_source", return_value=MOCK_WEATHER):
        rows = list(weather.get_lines())

    expected = [
        "Hour  Weather        Temp Hum Rain Wind ",
        "12:00 Slight Rain    18°C 55% 2mm  3m/s ",
        "13:00 Slight Rain    19°C 52% 2mm  3m/s ",
        "14:00 Cloudy         19°C 51%      4m/s ",
        "15:00 Sunny          20°C 52%      1m/s ",
        "16:00 Sunny          21°C 52%      1m/s ",
        "17:00 Very Sunny     23°C 49%      2m/s ",
        "18:00 Overcast Clo.. 22°C 51% 2mm  2m/s ",
        "19:00 Tropical Storm 26°C 89% 54mm 27m/s",
    ]

    assert rows == expected


@freeze_time("2020-01-01", tz_offset=0)
def test_weather_skip_header() -> None:
    weather = Weather(
        20, 45, lat="1", lon="1", api_key="", rows=10, every_hours=3, header=False
    )
    with mock.patch.object(weather, "_get_source", return_value=MOCK_WEATHER):
        rows = list(weather.get_lines())

    expected = [
        "12:00 Slight Rain         18°C 55% 2mm  3m/s ",
        "15:00 Sunny               20°C 52%      1m/s ",
        "18:00 Overcast Clouds     22°C 51% 2mm  2m/s ",
    ]

    assert rows == expected
