from uagents import Agent, Context
from models import SatelliteRequest, SatelliteResponse
import os
from supabase import create_client, Client
import ee
ee.Initialize(project="farmer-insights-project")

# Initialize our Supabase client
url: str = "https://hpcqmlskbyotkpgljslh.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhwY3FtbHNrYnlvdGtwZ2xqc2xoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE0MTM5ODEsImV4cCI6MjA3Njk4OTk4MX0.PCAZxnWnKSpCzgZQRz5Pfl3oHHm3H1kh231rgi0zj2M"
supabase_client: Client = create_client(supabase_url=url, supabase_key=key)

agent = Agent(name="satellite_agent",
              seed="satellite_agent_seed_123",
              port=8002,
              endpoint=["http://127.0.0.1:8002/submit"]
              )


@agent.on_event("startup")
async def print_startup_message(ctx: Context):
    print(f"satellite data connected, {fetch_satellite_data("FARM01")}")
    ctx.logger.info(agent.address)

@agent.on_message(model=SatelliteRequest, replies=SatelliteResponse)
async def handle_satellite_request(ctx: Context, sender: str, msg: SatelliteRequest):
    ctx.logger.info(f"Received satellite request from {sender}: {msg.latitude}, {msg.longitude}")
    
    # Now, using Google Earth Engine to get satellite data.
    # Essentially, it's gonna be NDWI/NDVI data on a per-farm basis
    # So, every entry in this database is gonna focus on an X by X acre area of
    # farm. The mean, median NDVI and NDWI of that area will be used to determine
    # the health of the farm.
    response = SatelliteResponse(
        status=f"satellite data connected, {fetch_satellite_data("FARM01")}"
    )
    
    ctx.logger.info(f"Sending satellite response to {sender}: {response.status}")
    await ctx.send(
        sender, response
    )

# Farm IDs correspond to the names of the farms stored in the
# database. This function takes a farm ID and returns the satellite data for that farm,
# including lat/lon, NDWI, NDVI, and other important info
def fetch_satellite_data(farm_id: str):
    aggregate_block = supabase_client.table("satellite_data_table").select("id").execute()
    print(f"Aggregate block: {aggregate_block.data}")
    # relevant_latitude = aggregate_block["latitude"]
    # relevant_longitude = aggregate_block["longitude"]

    relevant_latitude = -122;
    relevant_longitude = 37;

    print(f"Farm ID labeled ", farm_id, "has latitude ", relevant_latitude, "and longitude ", relevant_longitude)
    # Define point of interest
    point = ee.Geometry.Point([relevant_latitude, relevant_longitude])

    # Load Landsat 8 TOA
    l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA')

    # Filter by date and location, get least cloudy image
    img = (l8.filterBounds(point)
        .filterDate('2015-01-01', '2015-12-31')
        .sort('CLOUD_COVER')
        .first())

    nir = img.select('B5')
    red = img.select('B4')
    green = img.select('B3')

    ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
    ndwi = nir.subtract(green).divide(nir.add(green)).rename('NDWI')

    task = ee.batch.Export.image.toDrive(
        image=ndvi,
        description='ndvi_image',
        folder='GEE_Exports',       # Google Drive folder
        fileNamePrefix='ndvi_2015',
        region=point.buffer(1000).bounds().getInfo()['coordinates'],  # 1km buffer
        scale=1,
        crs='EPSG:4326'
    )
    task.start()

    url = ndvi.getThumbURL({
        'min': 0,
        'max': 1,
        'palette': [
            'E6FFFF',
            'B3F0FF',
            '66E0FF',
            '33CCFF',
            '0099CC',
            '0066B2',
            '003F7F',
            '001B4D',
            '0A0A1F',
            '000000'
        ],
        'region': point.buffer(1000).bounds().getInfo()['coordinates'],
        'dimensions': 512
    })

    print(f"URL: {url}")

   
    satellite_data_block = {
        "mean_ndwi": 0.5,
        "mean_ndvi": 0.5,
        "median_ndwi": 0.5,
        "median_ndvi": 0.5,
        "min_ndwi": 0.5,
        "min_ndvi": 0.5,
        "max_ndwi": 0.5,
        "max_ndvi": 0.5,
    }

    return aggregate_block

# Writes a fetched block of satellite data to the database
async def write_satellite_data_to_database(farm_id: str, satellite_data: dict):
    aggregate_block = fetch_satellite_data()
    pass

if __name__ == "__main__":
    agent.run()