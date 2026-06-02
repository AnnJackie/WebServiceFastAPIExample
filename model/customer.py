from enum import Enum
from typing import Optional
from pydantic import BaseModel

class CustomerStatus(Enum):
    VIP = "VIP"
    REGULAR = "REGULAR"

class Customer(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    status: CustomerStatus
