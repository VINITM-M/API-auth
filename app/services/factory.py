
from services.openmeto_client import OpenMeteoClient 

_weather_client = None

def get_weather_client():

    global _weather_client

    if _weather_client is None:
        _weather_client = OpenMeteoClient()
    return _weather_client