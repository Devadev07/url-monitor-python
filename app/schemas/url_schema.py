from pydantic import BaseModel

class URLCreate(BaseModel):
    address: str
    check_interval: int
