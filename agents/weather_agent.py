from uagents import Agent, Context
from models import WeatherRequest, WeatherResponse

agent = Agent(name="weather_agent",
              seed="weather_agent_seed_123",
              port=8001,
              endpoint=["http://127.0.0.1:8001/submit"]
              )



@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)
 
 
@agent.on_message(model=WeatherRequest, replies=WeatherResponse)
async def handle_weather_request(ctx: Context, sender: str, msg: WeatherRequest):
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