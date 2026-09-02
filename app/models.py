from pydantic import BaseModel, Field, confloat

class WeatherMeta(BaseModel): 

    cached: bool = Field(..., description="Whether the response was served from cache")
    cache_time: Optional[str] = Field(None, description="Time when the data was cached")
    provider: str = Field("OpenMeteo", description="Weather data provider")  # Updated default provider
    data_type: str = Field(..., description="Type of data (current/historical/forecast/stats)")