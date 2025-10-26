from uagents import Agent, Context
from models import WeatherRequest, WeatherResponse
import requests

agent = Agent(name="weather_agent",
              seed="weather_agent_seed_123",
              port=8001,
              endpoint=["http://127.0.0.1:8001/submit"]
              )


def wind_direction_from_degrees(degrees):
    """Convert wind direction in degrees to cardinal direction."""
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]


def fetch_weather_data(latitude: float, longitude: float):
    """Fetch weather data from Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,uv_index_max",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)
 
 
@agent.on_message(model=WeatherRequest, replies=WeatherResponse)
async def handle_weather_request(ctx: Context, sender: str, msg: WeatherRequest):
    ctx.logger.info(f"Received weather request from {sender}: {msg.latitude}, {msg.longitude}")
    
    try:
        data = fetch_weather_data(msg.latitude, msg.longitude)
        
        current = data["current"]
        daily = data["daily"]
        
        forecast = WeatherResponse(
            temperature_high=daily["temperature_2m_max"][0],
            temperature_low=daily["temperature_2m_min"][0],
            humidity=current["relative_humidity_2m"],
            precipitation_chance=daily["precipitation_probability_max"][0] if daily["precipitation_probability_max"][0] else 0.0,
            wind_speed=current["wind_speed_10m"],
            wind_direction=wind_direction_from_degrees(current["wind_direction_10m"]),
            condition=str(current["weather_code"]),
            uv_index=int(daily["uv_index_max"][0]) if daily["uv_index_max"][0] else 0,
            visibility=10.0
        )
        
        ctx.logger.info(f"Sending weather forecast to {sender}")
        ctx.logger.info(f"Forecast: Code {forecast.condition}, High: {forecast.temperature_high}°F, Low: {forecast.temperature_low}°F")
        await ctx.send(sender, forecast)
        
    except Exception as e:
        ctx.logger.error(f"Error fetching weather data: {e}")


if __name__ == "__main__":
    agent.run()