from models.api_key import APIKey, generate_key
from schemas.api_key import table_insert


class APIKeyRepository:

    async def create(self, **fields) -> APIKey:
        
        # model class object 
        apikey = APIKey(**fields)

        #inserting into table
        table_insert(
            user_id=apikey.user_id,
            key=apikey.key,
            created_at=apikey.created_at,
            expires_at=apikey.expires_at,
            is_active=apikey.is_active,
            requests_count=apikey.requests_count or 0,
            max_requests=apikey.max_requests,
            reset_at=apikey.reset_at
        )
        return apikey
