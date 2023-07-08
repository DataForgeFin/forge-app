from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .address import Address


class Patient(BaseModel):
    patient_id: str
    name: str
    birthdate: datetime = None
    address: Optional[Address] = None
