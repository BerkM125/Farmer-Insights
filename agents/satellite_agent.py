from uagents import Agent, Context
from models import SatelliteRequest, SatelliteResponse

agent = Agent(name="satellite_agent",
              seed="satellite_agent_seed_123",
              port=8002,
              endpoint=["http://127.0.0.1:8002/submit"]
              )


@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)


@agent.on_message(model=SatelliteRequest, replies=SatelliteResponse)
async def handle_satellite_request(ctx: Context, sender: str, msg: SatelliteRequest):
    ctx.logger.info(f"Received satellite request from {sender}: {msg.latitude}, {msg.longitude}")
    
    # Hardcoded response for now
    response = SatelliteResponse(
        status="satellite data connected"
    )
    
    ctx.logger.info(f"Sending satellite response to {sender}: {response.status}")
    await ctx.send(
        sender, response
    )


if __name__ == "__main__":
    agent.run()

