from pydantic import BaseModel, Field
from typing import List


# Weather Models
class WeatherRequest(BaseModel):
    latitude: float = Field(description="The latitude of the location")
    longitude: float = Field(description="The longitude of the location")


class WeatherResponse(BaseModel):
    temperature_high: float = Field(description="High temperature in Fahrenheit")
    temperature_low: float = Field(description="Low temperature in Fahrenheit")
    humidity: float = Field(description="Humidity percentage")
    precipitation_chance: float = Field(description="Chance of precipitation (0-100)")
    precipitation_sum: float = Field(description="Total precipitation amount in mm")
    wind_speed: float = Field(description="Wind speed in mph")
    wind_direction: str = Field(description="Wind direction")
    condition: str = Field(description="Weather condition (e.g., sunny, cloudy, rainy)")
    uv_index: int = Field(description="UV index (0-11+)")


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
