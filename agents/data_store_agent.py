from uagents import Agent, Context
from models import (
    WeatherRequest, WeatherResponse,
    SatelliteRequest, SatelliteResponse,
    MarketRequest, MarketResponse,
    SoilEnvironmentRequest, SoilEnvironmentResponse
)
from supabase import create_client, Client
from datetime import date
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

FARM_ID = os.getenv("FARM_ID", "default_farm")

agent = Agent(name="data_store_agent",
              seed="data_store_agent_seed_123",
              port=8000,
              endpoint=["http://127.0.0.1:8000/submit"]
              )

WEATHER_AGENT_ADDRESS = "agent1qga95re2thygqrydtytm5zhg03jqznf8r08cv34fhdmsakc2m07awm7dcv6"
SATELLITE_AGENT_ADDRESS = "agent1qt6uwy02w48l49z007txkyys63e9tj73up3am4ftakejlmx8aqev7jzf37m"
MARKET_AGENT_ADDRESS = "agent1q26j45u6rtm83csyqhre6l0qwmdc67y065emknmcv9wvhcltfte0zfa4s2r"
SOIL_ENVIRONMENT_AGENT_ADDRESS = "agent1q0j9fcj57s70sm00asqpr4zh08juxk3wzzxz2zh2hua7el0alu4l27t40st"

# Storage for collected responses
collected_data = {
    "weather": None,
    "satellite": None,
    "market": None,
    "soil_environment": None
}


def check_and_log_complete_data(ctx: Context):
    """Check if all data is collected and log it."""
    if all(value is not None for value in collected_data.values()):
        ctx.logger.info("=" * 60)
        ctx.logger.info("ALL DATA COLLECTED:")
        ctx.logger.info("=" * 60)
        ctx.logger.info(f"Complete Data Dictionary: {collected_data}")
        ctx.logger.info("=" * 60)
        
        # Insert weather data into Supabase
        try:
            weather = collected_data["weather"]
            
            weather_record = {
                "farm_id": FARM_ID,
                "temperature_high_f": weather["temperature_high"],
                "temperature_low_f": weather["temperature_low"],
                "humidity_percent": weather["humidity"],
                "rainfall_chance": weather["precipitation_chance"],
                "rainfall_amount_mm": weather["precipitation_sum"],
                "wind_speed_mph": weather["wind_speed"],
                "wind_direction": weather["wind_direction"],
                "condition": int(weather["condition"]),
                "uv_index": float(weather["uv_index"]),
                "date": date.today().isoformat()
            }
            
            # Upsert (insert or update if farm_id exists)
            result = supabase.table("weather_data").upsert(weather_record).execute()
            
            ctx.logger.info(f"✅ Weather data inserted to Supabase for farm: {FARM_ID}")
            ctx.logger.info(f"Record: {result.data}")
            
        except Exception as e:
            ctx.logger.error(f"❌ Error inserting to Supabase: {e}")
        
        # Reset for next collection
        for key in collected_data:
            collected_data[key] = None


# Create the requests (after class definitions)
WEATHER_REQUEST = WeatherRequest(latitude=40.7128, longitude=-74.0060)
SATELLITE_REQUEST = SatelliteRequest(latitude=40.7128, longitude=-74.0060)
MARKET_REQUEST = MarketRequest(crop_type="Wheat")
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
    ctx.logger.info(f"Received weather data from {sender}")
    collected_data["weather"] = data.model_dump()
    check_and_log_complete_data(ctx)


@agent.on_message(model=SatelliteResponse)
async def handle_satellite(ctx: Context, sender: str, data: SatelliteResponse):
    ctx.logger.info(f"Received satellite data from {sender}")
    collected_data["satellite"] = data.model_dump()
    check_and_log_complete_data(ctx)


@agent.on_message(model=MarketResponse)
async def handle_market(ctx: Context, sender: str, data: MarketResponse):
    ctx.logger.info(f"Received market data from {sender}")
    collected_data["market"] = data.model_dump()
    check_and_log_complete_data(ctx)


@agent.on_message(model=SoilEnvironmentResponse)
async def handle_soil_environment(ctx: Context, sender: str, data: SoilEnvironmentResponse):
    ctx.logger.info(f"Received soil environment data from {sender}")
    collected_data["soil_environment"] = data.model_dump()
    check_and_log_complete_data(ctx)


if __name__ == "__main__":
    agent.run()