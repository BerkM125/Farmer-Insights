from pydantic import BaseModel, Field
from uagents import Agent, Context, Protocol, Model
 
agent = Agent(name="weather_agent",
              seed="weather_agent_seed_123",
              port=8001,
              endpoint=["http://127.0.0.1:8001/submit"]
              )

class WeatherRequest(BaseModel):
    latitude: float = Field(
        description="The latitude of the location"
    )
    longitude: float = Field(
        description="The longitude of the location"
    )   

class WeatherResponse(BaseModel):
    temperature_high: float = Field(description="High temperature in Fahrenheit")
    temperature_low: float = Field(description="Low temperature in Fahrenheit")
    humidity: float = Field(description="Humidity percentage")
    precipitation_chance: float = Field(description="Chance of precipitation (0-100)")
    wind_speed: float = Field(description="Wind speed in mph")
    wind_direction: str = Field(description="Wind direction")
    condition: str = Field(description="Weather condition (e.g., sunny, cloudy, rainy)")
    uv_index: int = Field(description="UV index (0-11+)")
    visibility: float = Field(description="Visibility in miles")



@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)
 
 
@agent.on_message(model=WeatherRequest, replies=WeatherResponse)
async def answer_question(ctx: Context, sender: str, msg: WeatherRequest):
    ctx.logger.info(f"Received weather request from {sender}: {msg.latitude}, {msg.longitude}")
    
    # Hardcoded weather forecast stats
    forecast = WeatherResponse(
        temperature_high=72.0,
        temperature_low=55.0,
        humidity=65.0,
        precipitation_chance=20.0,
        wind_speed=7.5,
        wind_direction="NW",
        condition="Partly Cloudy",
        uv_index=6,
        visibility=10.0
    )
    
    ctx.logger.info(f"Sending weather forecast to {sender}")
    ctx.logger.info(f"Forecast: {forecast.condition}, High: {forecast.temperature_high}°F, Low: {forecast.temperature_low}°F")
    await ctx.send(
        sender, forecast
    )


if __name__ == "__main__":
    agent.run()