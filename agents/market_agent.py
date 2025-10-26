from uagents import Agent, Context
from models import MarketRequest, MarketResponse
import csv
import os

agent = Agent(name="market_agent",
              seed="market_agent_seed_123",
              port=8003,
              endpoint=["http://127.0.0.1:8003/submit"]
              )


def load_commodity_data():
    """Load commodity price data from CSV file."""
    csv_path = os.path.join(os.path.dirname(__file__), "data", "Commodity Prices - Sheet1.csv")
    commodity_data = {}
    
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            commodity_name = row['Commodities'].lower()
            commodity_data[commodity_name] = {
                'commodity': row['Commodities'],
                'units': row['Units'],
                'year_2021': float(row['2021']),
                'year_2022': float(row['2022']),
                'year_2023': float(row['2023']),
                'quarter_2024Q4': float(row['2024Q4']),
                'quarter_2025Q1': float(row['2025Q1']),
                'quarter_2025Q2': float(row['2025Q2']),
                'one_month_ago': float(row['9/1/2025(One Month Ago)']),
                'current': float(row['Current'])
            }
    
    return commodity_data


@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)


@agent.on_message(model=MarketRequest, replies=MarketResponse)
async def handle_market_request(ctx: Context, sender: str, msg: MarketRequest):
    ctx.logger.info(f"Received market request from {sender} for crop: {msg.crop_type}")
    
    try:
        # Load commodity data from CSV
        commodity_data = load_commodity_data()
        crop_name = msg.crop_type.lower()
        
        if crop_name in commodity_data:
            data = commodity_data[crop_name]
            response = MarketResponse(**data)
            ctx.logger.info(f"Sending market data for {data['commodity']}: Current price ${data['current']} {data['units']}")
        else:
            # Return default data if crop not found
            ctx.logger.warning(f"Crop '{msg.crop_type}' not found in database")
            response = MarketResponse(
                commodity=msg.crop_type,
                units="N/A",
                year_2021=0.0,
                year_2022=0.0,
                year_2023=0.0,
                quarter_2024Q4=0.0,
                quarter_2025Q1=0.0,
                quarter_2025Q2=0.0,
                one_month_ago=0.0,
                current=0.0
            )
        
        await ctx.send(sender, response)
        
    except Exception as e:
        ctx.logger.error(f"Error loading commodity data: {e}")


if __name__ == "__main__":
    agent.run()

