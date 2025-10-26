from uagents import Agent, Context
from models import WeatherRequest, WeatherResponse, DailyWeather
import requests

agent = Agent(
    name="weather_agent",
    seed="weather_agent_seed_123",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)


def wind_direction_from_degrees(degrees):
    """Convert wind direction in degrees to cardinal direction."""
    directions = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    index = round(degrees / 22.5) % 16
    return directions[index]


def safe_get(data, key, index, default=0.0):
    """Safely get a value from daily data array with null checking."""
    if key not in data or not data[key] or len(data[key]) <= index:
        return default
    value = data[key][index]
    return value if value is not None else default


def create_daily_weather(daily_data, index):
    """Create a DailyWeather object from daily API data."""
    return DailyWeather(
        date=safe_get(daily_data, "time", index, ""),
        weather_code=int(safe_get(daily_data, "weather_code", index, 0)),
        temperature_high=safe_get(daily_data, "temperature_2m_max", index),
        temperature_low=safe_get(daily_data, "temperature_2m_min", index),
        temperature_mean=safe_get(daily_data, "temperature_2m_mean", index),
        precipitation_chance=safe_get(
            daily_data, "precipitation_probability_max", index
        ),
        precipitation_sum=safe_get(daily_data, "precipitation_sum", index),
        wind_speed_max=safe_get(daily_data, "wind_speed_10m_max", index),
        wind_gusts_max=safe_get(daily_data, "wind_gusts_10m_max", index),
        wind_direction=wind_direction_from_degrees(
            safe_get(daily_data, "wind_direction_10m_dominant", index)
        ),
        humidity_mean=safe_get(daily_data, "relative_humidity_2m_mean", index),
        evapotranspiration=safe_get(daily_data, "et0_fao_evapotranspiration", index),
        sunshine_duration=safe_get(daily_data, "sunshine_duration", index),
        dew_point=safe_get(daily_data, "dew_point_2m_mean", index),
    )


def fetch_weather_data(latitude: float, longitude: float):
    """Fetch weather data from Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,relative_humidity_2m_mean,et0_fao_evapotranspiration,temperature_2m_mean,precipitation_probability_max,sunshine_duration,dew_point_2m_mean",
        "timezone": "auto",
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)


@agent.on_message(model=WeatherRequest, replies=WeatherResponse)
async def handle_weather_request(ctx: Context, sender: str, msg: WeatherRequest):
    ctx.logger.info(
        f"Received weather request from {sender}: {msg.latitude}, {msg.longitude}"
    )

    try:
        data = fetch_weather_data(msg.latitude, msg.longitude)

        daily = data["daily"]

        # Build 7-day forecast
        daily_forecasts = []
        for i in range(min(7, len(daily["time"]))):
            day_forecast = create_daily_weather(daily, i)
            daily_forecasts.append(day_forecast)

        # Create response with 7-day forecast
        forecast = WeatherResponse(daily_forecast=daily_forecasts)

        ctx.logger.info(f"Sending 7-day weather forecast to {sender}")
        ctx.logger.info(f"Forecast includes {len(daily_forecasts)} days")
        await ctx.send(sender, forecast)

    except Exception as e:
        ctx.logger.error(f"Error fetching weather data: {e}")


if __name__ == "__main__":
    agent.run()
