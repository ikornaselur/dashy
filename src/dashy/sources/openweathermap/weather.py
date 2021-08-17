import datetime as dt
from typing import Dict, Iterator, Tuple

import requests

from dashy.sources import Source

URL = "https://api.openweathermap.org/data/2.5/onecall"

TIMESTAMP_WIDTH = 5
TEMP_WIDTH = 4
HUMIDITY_WIDTH = 3
RAIN_WIDTH = 4
WIND_WIDTH = 5


Row = Tuple[str, ...]


class Weather(Source):
    lat: str
    lon: str
    api_key: str
    rows: int
    every_hours: int
    header: bool

    def __init__(
        self,
        max_lines: int,
        max_width: int,
        *,
        lat: str,
        lon: str,
        api_key: str,
        rows: int = 5,
        every_hours: int = 3,
        header: bool = True,
    ) -> None:
        super().__init__(max_lines, max_width)
        self.lat = lat
        self.lon = lon
        self.api_key = api_key
        self.rows = rows
        self.every_hours = every_hours
        self.header = header

    def _get_source(self) -> Dict:
        response = requests.get(
            URL,
            params={
                "units": "metric",
                "lat": self.lat,
                "lon": self.lon,
                "exclude": "current,daily,alerts,minutely",
                "appid": self.api_key,
            },
        )
        response.raise_for_status()

        # TODO: Proper error handling
        return response.json()

    def _get_data(self) -> Iterator[Row]:
        data = self._get_source()
        hourly = data["hourly"]

        if self.header:
            yield ("Hour", "Weather", "Temp", "Hum", "Rain", "Wind")

        for hour in hourly[: self.rows * self.every_hours : self.every_hours]:
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

    def get_lines(self) -> Iterator[str]:
        weather_rows = self._get_data()

        title_width = (
            self.max_width
            - TIMESTAMP_WIDTH
            - TEMP_WIDTH
            - HUMIDITY_WIDTH
            - RAIN_WIDTH
            - WIND_WIDTH
            - 5  # Spaces between rows
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
