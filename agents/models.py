from pydantic import BaseModel, Field
from typing import List


# Weather Models
class WeatherRequest(BaseModel):
    latitude: float = Field(description="The latitude of the location")
    longitude: float = Field(description="The longitude of the location")


class DailyWeather(BaseModel):
    date: str = Field(description="Date of the forecast")
    weather_code: int = Field(description="WMO weather code (0-99)")
    temperature_high: float = Field(description="High temperature in Fahrenheit")
    temperature_low: float = Field(description="Low temperature in Fahrenheit")
    temperature_mean: float = Field(description="Mean temperature in Fahrenheit")
    precipitation_chance: float = Field(description="Chance of precipitation (0-100)")
    precipitation_sum: float = Field(description="Total precipitation amount in inches")
    wind_speed_max: float = Field(description="Maximum wind speed in mph")
    wind_gusts_max: float = Field(description="Maximum wind gusts in mph")
    wind_direction: str = Field(description="Dominant wind direction")
    humidity_mean: float = Field(description="Mean relative humidity percentage")
    evapotranspiration: float = Field(description="Evapotranspiration in inches")
    sunshine_duration: float = Field(description="Sunshine duration in seconds")
    dew_point: float = Field(description="Dew point temperature in Fahrenheit")


class WeatherResponse(BaseModel):
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
