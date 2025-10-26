from pydantic import BaseModel, Field


# Weather Models
class WeatherRequest(BaseModel):
    latitude: float = Field(
        description="The latitude of the location"
    )
    longitude: float = Field(
        description="The longitude of the location"
    )   

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
    latitude: float = Field(
        description="The latitude of the location"
    )
    longitude: float = Field(
        description="The longitude of the location"
    )   

class SatelliteResponse(BaseModel):
    status: str = Field(
        description="Status of the satellite data connection"
    )


# Market Models
class MarketRequest(BaseModel):
    crop_type: str = Field(
        description="The type of crop to get market data for"
    )

class MarketResponse(BaseModel):
    commodity: str = Field(description="Name of the commodity")
    units: str = Field(description="Units of measurement")
    year_2021: float = Field(description="Price in 2021")
    year_2022: float = Field(description="Price in 2022")
    year_2023: float = Field(description="Price in 2023")
    quarter_2024Q4: float = Field(description="Price in 2024 Q4")
    quarter_2025Q1: float = Field(description="Price in 2025 Q1")
    quarter_2025Q2: float = Field(description="Price in 2025 Q2")
    one_month_ago: float = Field(description="Price one month ago (9/1/2025)")
    current: float = Field(description="Current price")


# Soil Environment Models
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

