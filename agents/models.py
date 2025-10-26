from pydantic import BaseModel, Field


# Weather Models
class WeatherRequest(BaseModel):
    latitude: float = Field(
        description="The latitude of the location"
    )
    longitude: float = Field(
        description="The longitude of the location"
    )   

class WeatherResponse(BaseModel):
    temperature_high: float = Field(description="High temperature in Fahrenheit")
    temperature_low: float = Field(description="Low temperature in Fahrenheit")
    humidity: float = Field(description="Humidity percentage")
    precipitation_chance: float = Field(description="Chance of precipitation (0-100)")
    wind_speed: float = Field(description="Wind speed in mph")
    wind_direction: str = Field(description="Wind direction")
    condition: str = Field(description="Weather condition (e.g., sunny, cloudy, rainy)")
    uv_index: int = Field(description="UV index (0-11+)")
    visibility: float = Field(description="Visibility in miles")


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
    market_data: str = Field(
        description="Market data for the requested crop"
    )


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

