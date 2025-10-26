from uagents import Agent, Context
from models import MarketRequest, MarketResponseV2, PriceRecord
import csv
import os
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

agent = Agent(name="market_agent_v2",
              seed="market_agent_v2_seed_123",
              port=8004,
              endpoint=["http://127.0.0.1:8004/submit"]
              )

# Month name to number mapping
MONTH_MAP = {
    'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
    'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
    'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
}


def convert_period_to_date(year, period):
    """Convert year and period (e.g., 2025, 'APR') to date string 'YYYY-MM'."""
    month = MONTH_MAP.get(period.upper())
    if not month:
        return None
    return f"{year}-{month}"


def is_base_crop_price(data_item, commodity):
    """
    Check if the data item is a base crop price (not a subtype).
    Example: "BARLEY - PRICE RECEIVED, MEASURED IN $ / BU" -> True
    Example: "BARLEY, FEED - PRICE RECEIVED, MEASURED IN $ / BU" -> False
    """
    # Pattern: COMMODITY - PRICE RECEIVED, MEASURED IN ...
    # Should NOT have a comma between commodity name and " - PRICE RECEIVED"
    pattern = rf"^{re.escape(commodity.upper())} - PRICE RECEIVED, MEASURED IN .+$"
    return bool(re.match(pattern, data_item))


def extract_unit(data_item):
    """Extract the unit from the Data Item field."""
    match = re.search(r'MEASURED IN (.+)$', data_item)
    if match:
        return match.group(1)
    return None


def load_crop_price_data(crop_type):
    """
    Load price data from CSV file for a specific crop type.
    Returns list of records with date, crop_name, unit, and price.
    Only includes data from the last 12 months.
    """
    csv_path = os.path.join(os.path.dirname(__file__), "data", "prices.csv")
    price_records = []
    
    # Calculate date 12 months ago
    twelve_months_ago = datetime.now() - relativedelta(months=12)
    
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            commodity = row['Commodity'].strip()
            
            # Case-insensitive crop matching
            if commodity.lower() != crop_type.lower():
                continue
            
            data_item = row['Data Item'].strip()
            
            # Only include base crop prices (no subtypes)
            if not is_base_crop_price(data_item, commodity):
                continue
            
            # Convert date
            year = row['Year']
            period = row['Period']
            date_str = convert_period_to_date(year, period)
            
            if not date_str:
                continue
            
            # Filter for last 12 months
            record_date = datetime.strptime(date_str + '-01', '%Y-%m-%d')
            if record_date < twelve_months_ago:
                continue
            
            # Extract unit
            unit = extract_unit(data_item)
            if not unit:
                continue
            
            # Get price value
            price_value = row['Value'].strip()
            
            # Skip if price is not a valid number
            try:
                price = float(price_value)
            except (ValueError, TypeError):
                continue
            
            price_records.append({
                'date': date_str,
                'crop_name': commodity.lower(),
                'unit': unit,
                'price': price
            })
    
    return price_records


@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(f"Market Agent V2 Address: {agent.address}")


@agent.on_message(model=MarketRequest, replies=MarketResponseV2)
async def handle_market_request(ctx: Context, sender: str, msg: MarketRequest):
    """
    Handle market request by fetching crop price data from CSV (treated as API)
    and storing it in Supabase database.
    """
    ctx.logger.info(f"Received market request from {sender} for crop: {msg.crop_type}")
    
    try:
        # "Fetch" data from the "API" (CSV file)
        price_records = load_crop_price_data(msg.crop_type)
        
        if not price_records:
            ctx.logger.warning(f"No price data found for crop '{msg.crop_type}' in the last 12 months")
            # Send back empty response
            response = MarketResponseV2(
                crop_name=msg.crop_type.lower(),
                unit="N/A",
                records_count=0,
                price_records=[],
                latest_price=0.0,
                latest_date="N/A",
                status="no_data"
            )
            await ctx.send(sender, response)
            return
        
        ctx.logger.info(f"Found {len(price_records)} price records for {msg.crop_type}")
        
        # Store records in Supabase
        for record in price_records:
            try:
                result = supabase.table("market_prices").upsert(
                    record,
                    on_conflict="date,crop_name"
                ).execute()
                ctx.logger.info(f"✅ Stored price record: {record['date']} - {record['crop_name']} - ${record['price']} {record['unit']}")
            except Exception as e:
                ctx.logger.error(f"❌ Error inserting record to Supabase: {e}")
        
        # Prepare response with all price records
        latest_record = max(price_records, key=lambda x: x['date'])
        
        # Convert price records to PriceRecord models
        price_record_list = [
            PriceRecord(date=record['date'], price=record['price'])
            for record in sorted(price_records, key=lambda x: x['date'])
        ]
        
        response = MarketResponseV2(
            crop_name=latest_record['crop_name'],
            unit=latest_record['unit'],
            records_count=len(price_records),
            price_records=price_record_list,
            latest_price=latest_record['price'],
            latest_date=latest_record['date'],
            status="success"
        )
        
        ctx.logger.info(f"📊 Sending response: {len(price_record_list)} records, latest: ${latest_record['price']} on {latest_record['date']}")
        await ctx.send(sender, response)
        
    except Exception as e:
        ctx.logger.error(f"Error processing market request: {e}")
        import traceback
        ctx.logger.error(traceback.format_exc())


if __name__ == "__main__":
    agent.run()

