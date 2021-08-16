import datetime as dt
import os
from typing import Dict, Iterator, Tuple

import requests

URL = "https://api.openweathermap.org/data/2.5/onecall"

TIMESTAMP_WIDTH = 5
TEMP_WIDTH = 4
HUMIDITY_WIDTH = 3
RAIN_WIDTH = 4
WIND_WIDTH = 5


Row = Tuple[str, ...]


def _get_source() -> Dict:
    response = requests.get(
        URL,
        params={
            "units": "metric",
            "lat": os.environ["OPENWEATHERMAP_LAT"],  # TODO: Move to config
            "lon": os.environ["OPENWEATHERMAP_LON"],
            "exclude": "current,daily,alerts,minutely",
            "appid": os.environ["OPENWEATHERMAP_API_KEY"],
        },
    )
    response.raise_for_status()

    # TODO: Proper error handling
    return response.json()


def _get_data(
    rows: int = 5, every_hours: int = 3, header: bool = True
) -> Iterator[Row]:
    data = _get_source()
    hourly = data["hourly"]

    if header:
        yield ("Hour", "Weather", "Temp", "Hum", "Rain", "Wind")

    for hour in hourly[: rows * every_hours : every_hours]:
        timestamp = dt.datetime.fromtimestamp(hour["dt"]).strftime("%H:%M")
        temp = f"{hour['temp']:.0f}°C"
        humidity = f"{hour['humidity']}%"
        wind = f"{hour['wind_speed']:.0f}m/s"

        weather = hour["weather"][0]
        rain = f"{hour['rain']['1h']:.0f}mm" if "rain" in hour else ""

        yield (
            timestamp,
            weather["description"].title(),
            temp,
            humidity,
            rain,
            wind,
        )


def get_weather(
    max_width: int, *, rows: int = 5, every_hours: int = 3, header: bool = True
) -> Iterator[str]:
    weather_rows = _get_data(rows, every_hours, header)

    title_width = (
        max_width
        - TIMESTAMP_WIDTH
        - TEMP_WIDTH
        - HUMIDITY_WIDTH
        - RAIN_WIDTH
        - WIND_WIDTH
        - 5  # Spaces
    )

    for timestamp, title, temp, humidity, rain, wind in weather_rows:
        if len(title) > title_width:
            title = f"{title[:title_width - 2]}.."

        yield (
            f"{timestamp:<{TIMESTAMP_WIDTH}} "
            f"{title:<{title_width}} "
            f"{temp:<{TEMP_WIDTH}} "
            f"{humidity:<{HUMIDITY_WIDTH}} "
            f"{rain:<{RAIN_WIDTH}} "
            f"{wind:<{WIND_WIDTH}}"
        )
