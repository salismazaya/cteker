from pydantic import BaseModel

class Transfer(BaseModel):
    network_id: str
    receipent: str
    amount: float
    signature: str
    unique: str
    gas: int = 21_000