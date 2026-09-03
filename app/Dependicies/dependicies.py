from fastapi import HTTPException, Header


async def verify_api_key(
        x_api_key: str = Header(..., alias="X-API-Key")):
    
    if not x_api_key:
        raise HTTPException(status_code=400, detail="X-API-Key header missing") 
    return x_api_key 