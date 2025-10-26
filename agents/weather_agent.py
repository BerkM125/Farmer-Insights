from uagents import Agent, Context
from models import WeatherRequest, WeatherResponse, DailyWeather
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
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,uv_index_max",
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
        
        # Build 7-day forecast
        daily_forecasts = []
        for i in range(7):
            day_forecast = DailyWeather(
                date=daily["time"][i],
                temperature_high=daily["temperature_2m_max"][i],
                temperature_low=daily["temperature_2m_min"][i],
                precipitation_chance=daily["precipitation_probability_max"][i] if daily["precipitation_probability_max"][i] else 0.0,
                precipitation_sum=daily["precipitation_sum"][i] if daily["precipitation_sum"][i] else 0.0,
                uv_index=int(daily["uv_index_max"][i]) if daily["uv_index_max"][i] else 0,
            )
            daily_forecasts.append(day_forecast)
        
        forecast = WeatherResponse(
            current_humidity=current["relative_humidity_2m"],
            current_wind_speed=current["wind_speed_10m"],
            current_wind_direction=wind_direction_from_degrees(current["wind_direction_10m"]),
            current_condition=str(current["weather_code"]),
            daily_forecast=daily_forecasts
        )
        
        ctx.logger.info(f"Sending 7-day weather forecast to {sender}")
        ctx.logger.info(f"Current: Code {forecast.current_condition}, Humidity: {forecast.current_humidity}%")
        await ctx.send(sender, forecast)
        
    except Exception as e:
        ctx.logger.error(f"Error fetching weather data: {e}")


if __name__ == "__main__":
    agent.run()