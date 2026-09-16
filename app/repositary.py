from models.api_key import APIKey, generate_key
from db.table_insertion import api_info_table_insert


class APIKeyRepository:

    async def create(self, payload) -> APIKey:

        # here, we're definig the class objects for each feilds into the table insertion 
        data = payload.model_dump() if hasattr(payload, "model_dump") else (payload.dict() if hasattr(payload, "dict") else dict(payload))
        apikey = APIKey(**data)

        # inserting into api key table  where we stores all the info about the api key  
        api_info_table_insert(
            user_id=apikey.user_id,
            key=apikey.key,
            created_at=apikey.created_at,
            expires_at=apikey.expires_at,
            is_active=apikey.is_active,
            requests_count=apikey.requests_count or 0,
            max_requests=apikey.max_requests,
            reset_at=apikey.reset_at,
        )
        
        return apikey 
