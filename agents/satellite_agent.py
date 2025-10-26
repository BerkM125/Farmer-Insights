from uagents import Agent, Context
from models import SatelliteRequest, SatelliteResponse
import os
from supabase import create_client, Client
import ee
from dotenv import load_dotenv

load_dotenv()

ee.Authenticate()

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

# Defines a global buffer radius for all satellite data calculations
BUFFER_RADIUS = 3000


def get_ndwi_map_url(latitude: float, longitude: float) -> tuple[ee.Image, str]:
    """
    Generates NDWI (Normalized Difference Water Index) map URL using Landsat 8 data.
    Returns a water resources map with drought (black) to saturated (blue) color scheme.
    """
    # Define point of interest
    point = ee.Geometry.Point([latitude, longitude])

    # Load Landsat 8 TOA
    l8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA")

    # Filter by date and location, get least cloudy image
    img = (
        l8.filterBounds(point)
        .filterDate("2025-01-01", "2025-10-01")
        .sort("CLOUD_COVER")
        .first()
    )

    # Get required bands
    nir = img.select("B5")
    green = img.select("B3")

    # Calculate NDWI
    ndwi = nir.subtract(green).divide(nir.add(green)).rename("NDWI")

    # Export to Google Drive
    task = ee.batch.Export.image.toDrive(
        image=ndwi,
        description="landsat8_ndwi_water_resources",
        folder="GEE_Exports",
        fileNamePrefix=f"ndwi_water_{latitude}_{longitude}",
        region=point.buffer(BUFFER_RADIUS).bounds().getInfo()["coordinates"],
        scale=30,
        crs="EPSG:4326",
    )
    task.start()

    # Generate thumbnail URL with app color scheme: black to teal
    url = ndwi.getThumbURL(
        {
            "min": -1.0,  # NDWI range: -1 (dry) to +1 (wet)
            "max": 1.0,
            "palette": [
                "#000000",  # black - dry/low water
                "#39c6af",  # blue-1 (teal) - saturated/high water
            ],
            "region": point.buffer(BUFFER_RADIUS).bounds().getInfo()["coordinates"],
            "dimensions": 2056,
        }
    )

    return (ndwi, url)


def get_ndvi_map_url(latitude: float, longitude: float) -> tuple[ee.Image, str]:
    """
    Generates NDVI (Normalized Difference Vegetation Index) map URL using Landsat 8 data.
    Returns a vegetation health map with green-themed color palette.
    """
    # Define point of interest
    point = ee.Geometry.Point([latitude, longitude])

    # Load Landsat 8 TOA
    l8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA")

    # Filter by date and location, get least cloudy image
    img = (
        l8.filterBounds(point)
        .filterDate("2024-01-01", "2024-12-31")
        .sort("CLOUD_COVER")
        .first()
    )

    # Get required bands
    nir = img.select("B5")
    red = img.select("B4")

    # Calculate NDVI
    ndvi = nir.subtract(red).divide(nir.add(red)).rename("NDVI")

    # Export to Google Drive
    task = ee.batch.Export.image.toDrive(
        image=ndvi,
        description="landsat8_ndvi_vegetation_health",
        folder="GEE_Exports",
        fileNamePrefix=f"ndvi_vegetation_{latitude}_{longitude}",
        region=point.buffer(BUFFER_RADIUS).bounds().getInfo()["coordinates"],
        scale=30,
        crs="EPSG:4326",
    )
    task.start()

    # Generate thumbnail URL with app color scheme
    url = ndvi.getThumbURL(
        {
            "min": -0.2,  # NDVI range for Landsat 8
            "max": 1.0,
            "palette": [
                "#e06c6c",  # red-1 - bare soil/poor vegetation
                "#dbba57",  # yellow-1 - moderate vegetation
                "#97c639",  # green-1 - healthy vegetation
                "#39c6af",  # blue-1 - very healthy/dense vegetation
            ],
            "region": point.buffer(BUFFER_RADIUS).bounds().getInfo()["coordinates"],
            "dimensions": 2056,
        }
    )

    return (ndvi, url)


agent = Agent(
    name="satellite_agent",
    seed="satellite_agent_seed_123",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
)


@agent.on_event("startup")
async def print_startup_message(ctx: Context):
    print(f"satellite data connected, {fetch_satellite_data('FARM01')}")
    ctx.logger.info(agent.address)


@agent.on_message(model=SatelliteRequest, replies=SatelliteResponse)
async def handle_satellite_request(ctx: Context, sender: str, msg: SatelliteRequest):
    ctx.logger.info(
        f"Received satellite request from {sender}: {msg.latitude}, {msg.longitude}"
    )

    # Now, using Google Earth Engine to get satellite data.
    # Essentially, it's gonna be NDWI/NDVI data on a per-farm basis
    # So, every entry in this database is gonna focus on an X by X acre area of
    # farm. The mean, median NDVI and NDWI of that area will be used to determine
    # the health of the farm.
    response = SatelliteResponse(
        status=f"satellite data connected, {fetch_satellite_data('FARM01')}"
    )

    ctx.logger.info(f"Sending satellite response to {sender}: {response.status}")
    await ctx.send(sender, response)


# Farm IDs correspond to the names of the farms stored in the
# database. This function takes a farm ID and returns the satellite data for that farm,
# including lat/lon, NDWI, NDVI, and other important info
def fetch_satellite_data(farm_id: str):
    aggregate_block = (
        supabase_client.table("satellite_data_table").select("*").execute()
    )
    print(f"Aggregate block: {aggregate_block.data}")

    relevant_latitude = aggregate_block.data[0]["latitude"]
    relevant_longitude = aggregate_block.data[0]["longitude"]

    print(
        f"Farm ID labeled ",
        farm_id,
        "has latitude ",
        relevant_latitude,
        "and longitude ",
        relevant_longitude,
    )

    # Get both map URLs
    ndwi, water_url = get_ndwi_map_url(relevant_latitude, relevant_longitude)
    ndvi, vegetation_url = get_ndvi_map_url(relevant_latitude, relevant_longitude)

    print(f"Water Resources Map URL: {water_url}")
    print(f"Vegetation Health Map URL: {vegetation_url}")

    ndwi_stats = get_normalized_diff_stats(relevant_latitude, relevant_longitude, ndwi)
    ndvi_stats = get_normalized_diff_stats(relevant_latitude, relevant_longitude, ndvi)

    print()
    print()
    print(f"NDWI Stats: {ndwi_stats}")
    print(f"NDVI Stats: {ndvi_stats}")
    print()
    print()

    satellite_data_block = {
        "latitude": relevant_latitude,
        "longitude": relevant_longitude,
        "mean_ndwi": ndwi_stats["NDWI_mean"],
        "mean_ndvi": ndvi_stats["NDVI_mean"],
        "median_ndwi": ndwi_stats["NDWI_median"],
        "median_ndvi": ndvi_stats["NDVI_median"],
        "25th_ndwi": ndwi_stats["NDWI_p25"],
        "25th_ndvi": ndvi_stats["NDVI_p25"],
        "75th_ndwi": ndwi_stats["NDWI_p75"],
        "75th_ndvi": ndvi_stats["NDVI_p75"],
        "ndwi_url": water_url,
        "ndvi_url": vegetation_url,
    }

    # Crop advice needs to process the entire data block, only insert after
    # rest of data is already inserted / inputted.
    satellite_data_block["crop_advice"] = crop_advice(satellite_data_block)

    # Insert the satellite data block into the database
    result = (
        supabase_client.table("satellite_data_table")
        .update(satellite_data_block)
        .eq("id", 1)
        .execute()
    )
    print(f"Satellite data block updated into database: {result.data}")

    return aggregate_block


def get_normalized_diff_stats(
    latitude: float, longitude: float, nd_image: ee.Image
) -> dict:
    point = ee.Geometry.Point([latitude, longitude])

    stats = nd_image.reduceRegion(
        reducer=ee.Reducer.mean()
        .combine(ee.Reducer.median(), "", True)
        .combine(ee.Reducer.percentile([25, 75]), "", True),
        geometry=point.buffer(BUFFER_RADIUS),
        scale=30,
        maxPixels=1e9,
    )

    return stats.getInfo()


def get_crop_task_recs(satellite_data_block):
    # Return a list of strings that are recommendations for how to
    # treat the crop based on all the data this function recieves.
    # Should use an LLM instance to generate this tasklist.
    pass


def crop_advice(satellite_data_block):
    ndvi_mean = satellite_data_block["mean_ndvi"]
    ndvi_25 = satellite_data_block["25th_ndvi"]
    ndvi_75 = satellite_data_block["75th_ndvi"]

    ndwi_mean = satellite_data_block["mean_ndwi"]
    ndwi_25 = satellite_data_block["25th_ndwi"]
    ndwi_75 = satellite_data_block["75th_ndwi"]

    # Thresholds (adjustable based on local conditions)
    ndvi_low = 0.3
    ndvi_high = 0.7
    ndwi_low = 0.1
    ndwi_high = 0.5

    # Analyze water status
    if ndwi_mean < ndwi_low:
        water_status = "approaching drought; begin storing or irrigating water"
    elif ndwi_mean > ndwi_high:
        water_status = "water levels high; monitor for waterlogging"
    else:
        water_status = "moisture levels are adequate"

    # Analyze crop health
    if ndvi_mean < ndvi_low:
        crop_status = "plants are stressed; consider fertilization and pest management"
    elif ndvi_mean > ndvi_high:
        crop_status = "plants are healthy and growing well"
    else:
        crop_status = "plants are moderately healthy; monitor for stress signs"

    # Combine into a single advisory string
    advice = f"Water status: {water_status}. Crop status: {crop_status}."

    return advice


# Writes a fetched block of satellite data to the database
async def write_satellite_data_to_database(farm_id: str, satellite_data: dict):
    aggregate_block = fetch_satellite_data()
    pass


if __name__ == "__main__":
    agent.run()
