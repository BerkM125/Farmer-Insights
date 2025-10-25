import httpx
from pydantic import BaseModel, Field
from uagents import Agent, Context, Protocol, Model


agent = Agent(name="weather_agent",
              port=8000,
              endpoint=["http://127.0.0.1:8000/submit"]
              )


class WeatherRequest(BaseModel):
    latitude: float = Field(
        description="Latitude of the location"
    )
    longitude: float = Field(
        description="Longitude of the location"
    )


class WeatherResponse(BaseModel):
    forecast: str = Field(
        description="The weather forecast information"
    )


@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)
    latitude = 40.7128
    longitude = -74.0060
    ctx.logger.info(f"Fetching weather forecast for coordinates: {latitude}, {longitude}")
    forecast = await get_weather_forecast(latitude, longitude)
    ctx.logger.info(f"\n{forecast}")


async def get_weather_forecast(latitude: float, longitude: float):
    """Fetch weather forecast from Open-Meteo API"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "auto",
        "forecast_days": 3
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
    
    # Format the forecast
    current = data.get("current", {})
    daily = data.get("daily", {})
    
    forecast = f"Current Weather:\n"
    forecast += f"Temperature: {current.get('temperature_2m')}°F\n"
    forecast += f"Humidity: {current.get('relative_humidity_2m')}%\n"
    forecast += f"Wind Speed: {current.get('wind_speed_10m')} mph\n\n"
    
    forecast += "3-Day Forecast:\n"
    for i in range(len(daily.get("time", []))):
        date = daily["time"][i]
        temp_max = daily["temperature_2m_max"][i]
        temp_min = daily["temperature_2m_min"][i]
        precip = daily["precipitation_sum"][i]
        forecast += f"{date}: High {temp_max}°F, Low {temp_min}°F, Precipitation: {precip} in\n"
    
    return forecast


@agent.on_message(model=WeatherRequest, replies=WeatherResponse)
async def answer_question(ctx: Context, sender: str, msg: WeatherRequest):
    ctx.logger.info(f"Received weather request from {sender}: lat={msg.latitude}, lon={msg.longitude}")
    forecast = await get_weather_forecast(msg.latitude, msg.longitude)
    ctx.logger.info(f"Forecast: {forecast}")
    await ctx.send(
        sender, WeatherResponse(forecast=forecast)
    )
 
if __name__ == "__main__":
    agent.run()