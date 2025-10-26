from pydantic import BaseModel, Field
from uagents import Agent, Context, Protocol, Model

agent = Agent(name="soil_environment_agent",
              seed="soil_environment_agent_seed_123",
              port=8004,
              endpoint=["http://127.0.0.1:8004/submit"]
              )

class SoilEnvironmentRequest(BaseModel):
    latitude: float = Field(
        description="The latitude of the location"
    )
    longitude: float = Field(
        description="The longitude of the location"
    )

class SoilEnvironmentResponse(BaseModel):
    soil_data: str = Field(
        description="Soil and environment data for the requested location"
    )


@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)


@agent.on_message(model=SoilEnvironmentRequest, replies=SoilEnvironmentResponse)
async def handle_soil_request(ctx: Context, sender: str, msg: SoilEnvironmentRequest):
    ctx.logger.info(f"Received soil environment request from {sender}: {msg.latitude}, {msg.longitude}")
    
    # Hardcoded response
    response = SoilEnvironmentResponse(
        soil_data=f"Soil at location ({msg.latitude}, {msg.longitude}) has pH 6.5, high organic content, and optimal moisture levels."
    )
    
    ctx.logger.info(f"Sending soil environment response to {sender}")
    await ctx.send(
        sender, response
    )


if __name__ == "__main__":
    agent.run()

