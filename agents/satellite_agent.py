from pydantic import BaseModel, Field
from uagents import Agent, Context, Protocol, Model

agent = Agent(name="satellite_agent",
              seed="satellite_agent_seed_123",
              port=8002,
              endpoint=["http://127.0.0.1:8002/submit"]
              )

class SatelliteRequest(BaseModel):
    latitude: float = Field(
        description="The latitude of the location"
    )
    longitude: float = Field(
        description="The longitude of the location"
    )   

class SatelliteResponse(BaseModel):
    status: str = Field(
        description="Status of the satellite data connection"
    )


@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)


@agent.on_message(model=SatelliteRequest, replies=SatelliteResponse)
async def handle_satellite_request(ctx: Context, sender: str, msg: SatelliteRequest):
    ctx.logger.info(f"Received satellite request from {sender}: {msg.latitude}, {msg.longitude}")
    
    # Now, using Google Earth Engine to get satellite data.
    response = SatelliteResponse(
        status="satellite data connected"
    )
    
    ctx.logger.info(f"Sending satellite response to {sender}: {response.status}")
    await ctx.send(
        sender, response
    )


if __name__ == "__main__":
    agent.run()

