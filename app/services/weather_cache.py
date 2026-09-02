import json

from redis.asyncio import Redis, ConnectionPool
from models.weather import WeatherMeta 

class WeatherCache:

    def __init__(
            self,
            redis_host: str,
            redis_port: int,
            redis_db: int = 0,
            redis_password: Optional[str] = None
    ):

        self.pool = ConnectionPool(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                password=redis_password,
                decode_responses=True
            )
        self._redis: Optional[Redis] = None

    def _get_key(self, city: str, date: str, data_type: str) -> str:
        """Generate Redis key"""
        return f"weather:{city}:{date}:{data_type}"

    async def get_redis(self) -> Redis:
        """Get Redis connection from pool"""
        if self._redis is None or self._redis.connection is None:
            self._redis = Redis(connection_pool=self.pool)
        return self._redis

    async def get(self, city_key: str, date: str, weather_type: str, units: str):

        """Get weather data from cache and convert to requested units"""
        redis = await self.get_redis()
        key = self._get_key(city_key, date, weather_type)

        data = await redis.get(key)

        if data:
            try:
                json_data = json.loads(data)
                cached_units = json_data.get("units", "standard")

                # Add cache metadata
                meta = WeatherMeta(
                    cached=True,
                    cache_time=datetime.now().isoformat() + "Z",
                    provider="OpenMeteo",
                    data_type=data_type
                )

        