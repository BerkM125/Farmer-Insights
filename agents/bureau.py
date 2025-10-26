from uagents import Bureau
from weather_agent import agent as weather_agent
from satellite_agent import agent as satellite_agent
from market_agent import agent as market_agent
from soil_environment_agent import agent as soil_environment_agent
from data_store_agent import agent as data_store_agent


if __name__ == "__main__":
    bureau = Bureau(
        port=8888,
        endpoint=["http://127.0.0.1:8888/submit"]
    )
    bureau.add(weather_agent)
    bureau.add(satellite_agent)
    bureau.add(market_agent)
    bureau.add(soil_environment_agent)
    bureau.add(data_store_agent)
    bureau.run()

