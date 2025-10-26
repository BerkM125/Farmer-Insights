from pydantic import BaseModel, Field
from typing import List


# Weather Models
class WeatherRequest(BaseModel):
    latitude: float = Field(description="The latitude of the location")
    longitude: float = Field(description="The longitude of the location")


class DailyWeather(BaseModel):
    date: str = Field(description="Date of the forecast")
    temperature_high: float = Field(description="High temperature in Fahrenheit")
    temperature_low: float = Field(description="Low temperature in Fahrenheit")
    precipitation_chance: float = Field(description="Chance of precipitation (0-100)")
    precipitation_sum: float = Field(description="Total precipitation amount in mm")
    uv_index: int = Field(description="UV index (0-11+)")

class WeatherResponse(BaseModel):
    current_humidity: float = Field(description="Current humidity percentage")
    current_wind_speed: float = Field(description="Current wind speed in mph")
    current_wind_direction: str = Field(description="Current wind direction")
    current_condition: str = Field(description="Current weather condition code")
    daily_forecast: list[DailyWeather] = Field(description="7-day weather forecast")


# Satellite Models
class SatelliteRequest(BaseModel):
    latitude: float = Field(description="The latitude of the location")
    longitude: float = Field(description="The longitude of the location")


class SatelliteResponse(BaseModel):
    status: str = Field(description="Status of the satellite data connection")


# Market Models
class MarketRequest(BaseModel):
    crop_type: str = Field(description="The type of crop to get market data for")


class PriceRecord(BaseModel):
    date: str = Field(description="Date of the price record (YYYY-MM format)")
    price: float = Field(description="Price value")


class MarketResponseV2(BaseModel):
    crop_name: str = Field(description="Name of the crop (lowercase)")
    unit: str = Field(description="Unit of measurement (e.g., $ / BU)")
    records_count: int = Field(description="Number of price records returned")
    price_records: List[PriceRecord] = Field(
        description="List of monthly price records from last 12 months"
    )
    latest_price: float = Field(description="Most recent price")
    latest_date: str = Field(description="Date of most recent price (YYYY-MM format)")
    status: str = Field(description="Status message (e.g., 'success', 'no_data')")


# Soil Environment Models
class SoilEnvironmentRequest(BaseModel):
    latitude: float = Field(description="The latitude of the location")
    longitude: float = Field(description="The longitude of the location")


class SoilEnvironmentResponse(BaseModel):
    soil_data: str = Field(
        description="Soil and environment data for the requested location"
    )
