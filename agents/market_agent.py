from uagents import Agent, Context
from models import MarketRequest, MarketResponse

agent = Agent(name="market_agent",
              seed="market_agent_seed_123",
              port=8003,
              endpoint=["http://127.0.0.1:8003/submit"]
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

