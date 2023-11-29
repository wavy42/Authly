from typing import Optional, List
from pydantic import BaseModel


class Application(BaseModel):
    id: Optional[str] = None
    name: str
    version: str
    default_access: Optional[List[str]] = None


class ApplicationDB(BaseModel):
    bubble_id: str
    bubble_name: str
    applications: Optional[List[Application]]
