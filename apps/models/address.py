from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    state: Optional[str] = None
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
