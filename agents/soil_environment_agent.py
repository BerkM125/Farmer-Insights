from uagents import Agent, Context
from models import SoilEnvironmentRequest, SoilEnvironmentResponse
import ee
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

ee.Initialize(project="farmer-insights-project")


# Initialize our Supabase client with environment variables
def get_supabase_client() -> Client:
    """
    Initialize Supabase client using environment variables.

    Returns:
        Client: Initialized Supabase client

    Raises:
        ValueError: If required environment variables are missing
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url:
        raise ValueError("SUPABASE_URL environment variable is required but not set")
    if not key:
        raise ValueError("SUPABASE_KEY environment variable is required but not set")

    return create_client(supabase_url=url, supabase_key=key)


# Initialize Supabase client
supabase_client: Client = get_supabase_client()
BUFFER_RADIUS = 3000

agent = Agent(
    name="soil_environment_agent",
    seed="soil_environment_agent_seed_123",
    port=8004,
    endpoint=["http://127.0.0.1:8004/submit"],
)


@agent.on_event("startup")
async def print_address(ctx: Context):
    get_soil_ph(37.2787, -122.141153)
    ctx.logger.info(agent.address)


@agent.on_message(model=SoilEnvironmentRequest, replies=SoilEnvironmentResponse)
async def handle_soil_request(ctx: Context, sender: str, msg: SoilEnvironmentRequest):
    ctx.logger.info(
        f"Received soil environment request from {sender}: {msg.latitude}, {msg.longitude}"
    )

    # Hardcoded response
    response = SoilEnvironmentResponse(
        soil_data=f"Soil at location ({msg.latitude}, {msg.longitude}) has pH 6.5, high organic content, and optimal moisture levels."
    )

    ctx.logger.info(f"Sending soil environment response to {sender}")
    await ctx.send(sender, response)


def soil_advice(ph_stats: dict) -> str:
    """
    Analyzes pH statistics and provides immediate actionable advice for farmers.

    Args:
        ph_stats: Dictionary containing pH statistics (mean, median, p25, p75, etc.)

    Returns:
        String with immediate soil management advice
    """
    if not ph_stats or not isinstance(ph_stats, dict):
        return "Unable to analyze soil pH data. Please check soil sampling."

    # Extract pH values (assuming keys like 'phh2o_mean', 'phh2o_median', etc.)
    mean_ph = ph_stats.get("phh2o_0-5cm_mean_mean")
    median_ph = ph_stats.get("phh2o_0-5cm_mean_median")
    p75_ph = ph_stats.get("phh2o_0-5cm_mean_p75")
    p25_ph = ph_stats.get("phh2o_0-5cm_mean_p25")

    # Use mean pH as primary indicator, fallback to median
    primary_ph = mean_ph if mean_ph is not None else median_ph

    if primary_ph is None:
        return "Soil pH data unavailable. Please conduct soil testing."

    advice_parts = []

    # Primary pH analysis and immediate advice
    if primary_ph < 5.5:
        advice_parts.append(
            "🚨 SOIL IS HIGHLY ACIDIC - Apply lime immediately to raise pH to 6.0-6.5"
        )
        advice_parts.append("💡 Use dolomitic lime at 2-4 tons per acre")
        advice_parts.append("⚠️ Avoid planting acid-sensitive crops until pH improves")

    elif primary_ph < 6.0:
        advice_parts.append("⚠️ SOIL IS MODERATELY ACIDIC - Apply lime to raise pH")
        advice_parts.append("💡 Use calcitic lime at 1-2 tons per acre")
        advice_parts.append(
            "🌱 Consider acid-tolerant crops like blueberries or potatoes"
        )

    elif primary_ph > 8.0:
        advice_parts.append(
            "🚨 SOIL IS HIGHLY ALKALINE - Apply sulfur or acidifying fertilizers"
        )
        advice_parts.append("💡 Use elemental sulfur at 1-2 tons per acre")
        advice_parts.append(
            "🌿 Consider alkaline-tolerant crops like asparagus or spinach"
        )

    elif primary_ph > 7.5:
        advice_parts.append("⚠️ SOIL IS MODERATELY ALKALINE - Monitor pH closely")
        advice_parts.append("💡 Use ammonium-based fertilizers to slightly acidify")
        advice_parts.append("🌾 Most crops will grow well with minor adjustments")

    else:
        # pH between 6.0-7.5 (optimal range)
        advice_parts.append("✅ SOIL pH IS OPTIMAL - Maintain current levels")
        advice_parts.append("🌱 Perfect for most crops - no immediate action needed")
        advice_parts.append("📊 Continue regular pH monitoring")

    # Additional analysis based on pH variability
    if p25_ph is not None and p75_ph is not None:
        ph_range = p75_ph - p25_ph

        if ph_range > 1.5:
            advice_parts.append(
                "⚠️ HIGH pH VARIABILITY - Soil zones need different treatments"
            )
            advice_parts.append("🗺️ Consider zone-specific liming/acidification")

        elif ph_range > 1.0:
            advice_parts.append(
                "📊 MODERATE pH VARIABILITY - Monitor different field zones"
            )
            advice_parts.append("🌾 Adjust fertilizer rates by zone")

    # Specific crop recommendations based on pH
    if primary_ph < 6.0:
        advice_parts.append(
            "🌿 RECOMMENDED CROPS: Blueberries, potatoes, sweet potatoes, radishes"
        )
    elif primary_ph > 7.5:
        advice_parts.append(
            "🌿 RECOMMENDED CROPS: Asparagus, spinach, cabbage, broccoli"
        )
    else:
        advice_parts.append(
            "🌿 RECOMMENDED CROPS: Corn, soybeans, wheat, tomatoes, peppers"
        )

    # Timing advice
    advice_parts.append("⏰ BEST TIME TO APPLY: Fall or early spring before planting")
    advice_parts.append("🔄 RETEST SOIL: 3-6 months after treatment")

    # Join all advice parts
    full_advice = "\n".join(advice_parts)

    # Add summary
    summary = f"\n📋 SUMMARY: Soil pH {primary_ph:.1f} - "
    if primary_ph < 5.5:
        summary += "URGENT ACTION REQUIRED"
    elif primary_ph < 6.0 or primary_ph > 7.5:
        summary += "MODERATE ACTION NEEDED"
    else:
        summary += "MAINTAIN CURRENT CONDITIONS"

    return full_advice + summary


# Get the pH of the soil surrounding a geographic location, then
# return the image and its relevant URL
def get_soil_ph(latitude: float, longitude: float) -> tuple[ee.Image, dict]:
    point = ee.Geometry.Point([longitude, latitude])  # NOTE: EE uses [lon, lat]
    region = point.buffer(BUFFER_RADIUS)  # e.g., 3000 for 3 km

    # Load and clip topsoil pH
    soil_pH = (
        ee.Image("projects/soilgrids-isric/phh2o_mean")
        .select(0)
        .divide(10)
        .clip(region)
    )

    # Compute stats
    stats = soil_pH.reduceRegion(
        reducer=ee.Reducer.mean()
        .combine(ee.Reducer.median(), "", True)
        .combine(ee.Reducer.percentile([25, 75]), "", True),
        geometry=region,
        scale=250,
        maxPixels=1e9,
    ).getInfo()  # <-- converts ee.Dictionary to Python dict

    print("Soil pH statistics (0–5 cm):", stats)
    print(soil_advice(stats))

    ph_data_block = {
        "broad_advice": soil_advice(stats),
        "task_recommendations": soil_advice(stats).splitlines(),
        "nitrogen_levels": get_soil_nitrogen(latitude, longitude),
        "ph_url": "https://forages.oregonstate.edu/sites/forages.oregonstate.edu/files/styles/large/public/ph_map_usa.jpg.webp?itok=xyNyg9c4",  # TEMPORARY, FIX LATER
    }

    result = (
        supabase_client.table("environmental_data")
        .update(ph_data_block)
        .eq("farm_id", "FARM01")
        .execute()
    )

    return soil_pH, stats  # return the actual stats dictionary


def get_soil_nitrogen(latitude: float, longitude: float) -> list[float]:
    import random

    # Set random seed based on location for consistent results
    random.seed(int(latitude * longitude * 1000))

    # Simulate nitrogen levels over a growing season (120 days)
    days = 120
    nitrogen_levels = []

    # Base nitrogen level (varies by location)
    base_nitrogen = 80 + (latitude * 2) + (longitude * 1.5)  # Location-based variation

    for day in range(days):
        # Seasonal nitrogen depletion pattern
        # Nitrogen typically decreases over growing season due to plant uptake
        seasonal_factor = 1.0 - (day / days) * 0.4  # 40% depletion over season

        # Weekly fertilizer application cycles (every 14 days)
        fertilizer_boost = 0
        if day % 14 == 0:  # Fertilizer application days
            fertilizer_boost = random.uniform(20, 40)  # 20-40 ppm boost

        # Weather effects (rain can leach nitrogen)
        weather_factor = random.uniform(0.85, 1.15)  # ±15% variation

        # Plant growth phase effects
        if day < 30:  # Early growth - moderate uptake
            plant_uptake = day * 0.3
        elif day < 60:  # Peak growth - high uptake
            plant_uptake = 9 + (day - 30) * 0.8
        elif day < 90:  # Maturation - moderate uptake
            plant_uptake = 33 + (day - 60) * 0.4
        else:  # Late season - low uptake
            plant_uptake = 45 + (day - 90) * 0.1

        # Calculate nitrogen level for this day
        nitrogen_level = (
            base_nitrogen * seasonal_factor + fertilizer_boost
        ) * weather_factor - plant_uptake

        # Add some realistic noise
        noise = random.uniform(-5, 5)
        nitrogen_level += noise

        # Ensure nitrogen levels stay within realistic bounds (20-150 ppm)
        nitrogen_level = max(20, min(150, nitrogen_level))

        nitrogen_levels.append(round(nitrogen_level, 1))

    return nitrogen_levels


if __name__ == "__main__":
    agent.run()
