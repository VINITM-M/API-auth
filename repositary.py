from tkinter.tix import Select

from app.models.api_key import APIKey

class APIKeyRepository: 
    
    async def create(self, **fields) -> APIKey:
        """Create a new API key.

        Args:
            **fields: The fields to create the API key with.

        Returns:
            APIKey: The created API key.

        """

        api_key = APIKey(**fields) 

        return api_key 
