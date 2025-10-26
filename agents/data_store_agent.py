from uagents import Agent, Context
from models import (
    WeatherRequest, WeatherResponse,
    SatelliteRequest, SatelliteResponse,
    MarketRequest, MarketResponse,
    SoilEnvironmentRequest, SoilEnvironmentResponse
)

agent = Agent(name="data_store_agent",
              seed="data_store_agent_seed_123",
              port=8000,
              endpoint=["http://127.0.0.1:8000/submit"]
              )

WEATHER_AGENT_ADDRESS = "agent1qga95re2thygqrydtytm5zhg03jqznf8r08cv34fhdmsakc2m07awm7dcv6"
SATELLITE_AGENT_ADDRESS = "agent1qt6uwy02w48l49z007txkyys63e9tj73up3am4ftakejlmx8aqev7jzf37m"
MARKET_AGENT_ADDRESS = "agent1q26j45u6rtm83csyqhre6l0qwmdc67y065emknmcv9wvhcltfte0zfa4s2r"
SOIL_ENVIRONMENT_AGENT_ADDRESS = "agent1q0j9fcj57s70sm00asqpr4zh08juxk3wzzxz2zh2hua7el0alu4l27t40st"


# Create the requests (after class definitions)
WEATHER_REQUEST = WeatherRequest(latitude=40.7128, longitude=-74.0060)
SATELLITE_REQUEST = SatelliteRequest(latitude=40.7128, longitude=-74.0060)
MARKET_REQUEST = MarketRequest(crop_type="wheat")
SOIL_ENVIRONMENT_REQUEST = SoilEnvironmentRequest(latitude=40.7128, longitude=-74.0060)
 
 
@agent.on_event("startup")
async def ask_agents(ctx: Context):
    ctx.logger.info(f"Data Store Agent Address: {agent.address}")
    
    # Request weather data
    ctx.logger.info(f"Sending weather request to: {WEATHER_AGENT_ADDRESS}")
    ctx.logger.info(
        f"Asking weather agent for location: {WEATHER_REQUEST.latitude}, {WEATHER_REQUEST.longitude}"
    )
    await ctx.send(
        WEATHER_AGENT_ADDRESS, WEATHER_REQUEST
    )
    
    # Request satellite data
    ctx.logger.info(f"Sending satellite request to: {SATELLITE_AGENT_ADDRESS}")
    ctx.logger.info(
        f"Asking satellite agent for location: {SATELLITE_REQUEST.latitude}, {SATELLITE_REQUEST.longitude}"
    )
    await ctx.send(
        SATELLITE_AGENT_ADDRESS, SATELLITE_REQUEST
    )
    
    # Request market data
    ctx.logger.info(f"Sending market request to: {MARKET_AGENT_ADDRESS}")
    ctx.logger.info(
        f"Asking market agent for crop: {MARKET_REQUEST.crop_type}"
    )
    await ctx.send(
        MARKET_AGENT_ADDRESS, MARKET_REQUEST
    )
    
    # Request soil environment data
    ctx.logger.info(f"Sending soil environment request to: {SOIL_ENVIRONMENT_AGENT_ADDRESS}")
    ctx.logger.info(
        f"Asking soil environment agent for location: {SOIL_ENVIRONMENT_REQUEST.latitude}, {SOIL_ENVIRONMENT_REQUEST.longitude}"
    )
    await ctx.send(
        SOIL_ENVIRONMENT_AGENT_ADDRESS, SOIL_ENVIRONMENT_REQUEST
    )
 
 
@agent.on_message(model=WeatherResponse)
async def handle_weather(ctx: Context, sender: str, data: WeatherResponse):
    ctx.logger.info(f"Got weather forecast from {sender}:")
    ctx.logger.info(f"  Data: {data}")


@agent.on_message(model=SatelliteResponse)
async def handle_satellite(ctx: Context, sender: str, data: SatelliteResponse):
    ctx.logger.info(f"Got satellite response from {sender}:")
    ctx.logger.info(f"  Data: {data}")


@agent.on_message(model=MarketResponse)
async def handle_market(ctx: Context, sender: str, data: MarketResponse):
    ctx.logger.info(f"Got market response from {sender}:")
    ctx.logger.info(f"  Data: {data}")


@agent.on_message(model=SoilEnvironmentResponse)
async def handle_soil_environment(ctx: Context, sender: str, data: SoilEnvironmentResponse):
    ctx.logger.info(f"Got soil environment response from {sender}:")
    ctx.logger.info(f"  Data: {data}")


if __name__ == "__main__":
    agent.run()