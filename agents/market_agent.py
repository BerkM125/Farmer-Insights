from pydantic import BaseModel, Field
from uagents import Agent, Context, Protocol, Model

agent = Agent(name="market_agent",
              seed="market_agent_seed_123",
              port=8003,
              endpoint=["http://127.0.0.1:8003/submit"]
              )

class MarketRequest(BaseModel):
    crop_type: str = Field(
        description="The type of crop to get market data for"
    )

class MarketResponse(BaseModel):
    market_data: str = Field(
        description="Market data for the requested crop"
    )


@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)


@agent.on_message(model=MarketRequest, replies=MarketResponse)
async def handle_market_request(ctx: Context, sender: str, msg: MarketRequest):
    ctx.logger.info(f"Received market request from {sender} for crop: {msg.crop_type}")
    
    # Hardcoded response
    response = MarketResponse(
        market_data=f"Current market price for {msg.crop_type} is $250 per ton with high demand forecast."
    )
    
    ctx.logger.info(f"Sending market response to {sender}")
    await ctx.send(
        sender, response
    )


if __name__ == "__main__":
    agent.run()

