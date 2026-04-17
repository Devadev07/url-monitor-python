from pydantic import BaseModel

class URLCreate(BaseModel):
    address: str
    user_id: int