from uagents import Agent, Context
from models import (
    WeatherRequest,
    WeatherResponse,
    SatelliteRequest,
    SatelliteResponse,
    MarketRequest,
    MarketResponseV2,
    SoilEnvironmentRequest,
    SoilEnvironmentResponse,
)
from supabase import create_client, Client
from datetime import date, datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

FARM_ID = os.getenv("FARM_ID", "default_farm")

agent = Agent(
    name="data_store_agent",
    seed="data_store_agent_seed_123",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

WEATHER_AGENT_ADDRESS = (
    "agent1qga95re2thygqrydtytm5zhg03jqznf8r08cv34fhdmsakc2m07awm7dcv6"
)
SATELLITE_AGENT_ADDRESS = (
    "agent1qt6uwy02w48l49z007txkyys63e9tj73up3am4ftakejlmx8aqev7jzf37m"
)
MARKET_AGENT_ADDRESS = (
    "agent1q0z3dxx3huw6rq625s9vfke5w6drt80xdsjaelhqf6ga4rr9egze6vqysus"
)
SOIL_ENVIRONMENT_AGENT_ADDRESS = (
    "agent1q0j9fcj57s70sm00asqpr4zh08juxk3wzzxz2zh2hua7el0alu4l27t40st"
)

# Storage for collected responses
collected_data = {
    "weather": None,
    "satellite": None,
    "market": None,
    "soil_environment": None,
}


def check_and_log_complete_data(ctx: Context):
    """Check if weather data is collected and log it."""
    if collected_data["weather"] is not None:
        ctx.logger.info("=" * 60)
        ctx.logger.info("WEATHER DATA COLLECTED - PROCEEDING WITH DATABASE UPDATE:")
        ctx.logger.info("=" * 60)
        ctx.logger.info(f"Collected Data Dictionary: {collected_data}")
        ctx.logger.info("=" * 60)

        # Insert weather data into Supabase (7-day forecast)
        try:
            weather = collected_data["weather"]
            daily_forecast = weather["daily_forecast"]

            # Insert a row for each day in the 7-day forecast
            weather_records = []
            for day in daily_forecast:
                weather_record = {
                    "farm_id": FARM_ID,
                    "date": day["date"],
                    "weather_code": day["weather_code"],
                    "temperature_high": day["temperature_high"],
                    "temperature_low": day["temperature_low"],
                    "temperature_mean": day["temperature_mean"],
                    "precipitation_chance": day["precipitation_chance"],
                    "precipitation_sum": day["precipitation_sum"],
                    "wind_speed_max": day["wind_speed_max"],
                    "wind_gusts_max": day["wind_gusts_max"],
                    "wind_direction": day["wind_direction"],
                    "humidity_mean": day["humidity_mean"],
                    "evapotranspiration": day["evapotranspiration"],
                    "sunshine_duration": day["sunshine_duration"],
                    "dew_point": day["dew_point"],
                }
                weather_records.append(weather_record)

            # Upsert all records (insert or update if farm_id + date exists)
            result = supabase.table("weather_data").upsert(weather_records).execute()

            ctx.logger.info(f"✅ Weather data inserted to Supabase for farm: {FARM_ID}")
            ctx.logger.info(f"Inserted {len(weather_records)} daily forecast records")
            ctx.logger.info(f"Records: {result.data}")

        except Exception as e:
            ctx.logger.error(f"❌ Error inserting weather data to Supabase: {e}")

        # Insert market data into Supabase (one row per price data point)
        try:
            market = collected_data["market"]
            if market and market.get("price_records"):
                price_records = []
                for record in market["price_records"]:
                    price_record = {
                        "date": record["date"],
                        "crop_name": market["crop_name"],
                        "unit": market["unit"],
                        "price": record["price"],
                    }
                    price_records.append(price_record)

                # Upsert all records (insert or update if date + crop_name exists)
                result = (
                    supabase.table("market_prices")
                    .upsert(price_records, on_conflict="date,crop_name")
                    .execute()
                )

                ctx.logger.info(
                    f"✅ Market data inserted to Supabase for crop: {market['crop_name']}"
                )
                ctx.logger.info(f"Inserted {len(price_records)} price records")
                ctx.logger.info(
                    f"Date range: {price_records[0]['date']} to {price_records[-1]['date']}"
                )
            else:
                ctx.logger.warning("No market price records to insert")

        except Exception as e:
            ctx.logger.error(f"❌ Error inserting market data to Supabase: {e}")

        # Reset weather data for next collection
        collected_data["weather"] = None


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
    await ctx.send(WEATHER_AGENT_ADDRESS, WEATHER_REQUEST)

    # Request satellite data
    ctx.logger.info(f"Sending satellite request to: {SATELLITE_AGENT_ADDRESS}")
    ctx.logger.info(
        f"Asking satellite agent for location: {SATELLITE_REQUEST.latitude}, {SATELLITE_REQUEST.longitude}"
    )
    await ctx.send(SATELLITE_AGENT_ADDRESS, SATELLITE_REQUEST)

    # Request market data
    ctx.logger.info(f"Sending market request to: {MARKET_AGENT_ADDRESS}")
    ctx.logger.info(f"Asking market agent for crop: {MARKET_REQUEST.crop_type}")
    await ctx.send(MARKET_AGENT_ADDRESS, MARKET_REQUEST)

    # Request soil environment data
    ctx.logger.info(
        f"Sending soil environment request to: {SOIL_ENVIRONMENT_AGENT_ADDRESS}"
    )
    ctx.logger.info(
        f"Asking soil environment agent for location: {SOIL_ENVIRONMENT_REQUEST.latitude}, {SOIL_ENVIRONMENT_REQUEST.longitude}"
    )
    await ctx.send(SOIL_ENVIRONMENT_AGENT_ADDRESS, SOIL_ENVIRONMENT_REQUEST)


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


@agent.on_message(model=MarketResponseV2)
async def handle_market(ctx: Context, sender: str, data: MarketResponseV2):
    ctx.logger.info(f"Received market data from {sender}")
    collected_data["market"] = data.model_dump()
    check_and_log_complete_data(ctx)


@agent.on_message(model=SoilEnvironmentResponse)
async def handle_soil_environment(
    ctx: Context, sender: str, data: SoilEnvironmentResponse
):
    ctx.logger.info(f"Received soil environment data from {sender}")
    collected_data["soil_environment"] = data.model_dump()
    check_and_log_complete_data(ctx)


if __name__ == "__main__":
    agent.run()
