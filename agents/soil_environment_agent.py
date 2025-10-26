from uagents import Agent, Context
from models import SoilEnvironmentRequest, SoilEnvironmentResponse
import ee

agent = Agent(
    name="soil_environment_agent",
    seed="soil_environment_agent_seed_123",
    port=8004,
    endpoint=["http://127.0.0.1:8004/submit"],
)


@agent.on_event("startup")
async def print_address(ctx: Context):
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

def soil_advice():
    pass

# Get the pH of the soil surrounding a geographic location, then
# return the image and its relevant URL
def get_soil_ph(latitude: float, longitude: float) -> tuple[ee.Image, str]:
    # --- 1. Define location and region of interest ---
    point = ee.Geometry.Point([latitude, longitude]); # your coordinates
    region = point.buffer(3000); # 3 km radius

    # --- 2. Load SoilGrids pH dataset and process ---
    soil_pH = ee.Image('projects/soilgrids-isric/phh2o_mean').select(0).divide(10).clip(region);      # limit to region of interest

    # --- 3. Visualization parameters for pH ---
    ph_vis = {
        "min": 0,
        "max": 14,
        "palette": [
            'red',
            'orange',
            'yellow',
            'chartreuse',
            'green'
        ]
    }

    # --- 4. Compute statistics for the region ---
    stats = soil_pH.reduceRegion(
        reducer=ee.Reducer.mean()
                    .combine(ee.Reducer.median(), '', True)
                    .combine(ee.Reducer.percentile([25, 75]), '', True),
        geometry=region,
        scale=250,
        maxPixels=1e9
    )

    print('Soil pH statistics (0–5 cm):', stats);

    # Generate a map tile layer for pH
    visParams = {
        "min": 4,
        "max": 8,
        "palette": ['red', 'yellow', 'green']
    }

    map = soil_pH.getMap(visParams);
    print('Tile URL:', map.urlFormat);

    return (soil_pH, stats.getInfo())

if __name__ == "__main__":
    agent.run()
