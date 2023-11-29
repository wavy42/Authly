from typing import Dict, Optional, List
from pydantic import BaseModel


class ApplicationsKey(BaseModel):
    application: str
    duration_in_min: int
    valid_from: Optional[str]
    valid_to: Optional[str]

    strict: bool
    # only allows to use the key in this timespan (login to app)
    # key can be "activated/redeemed" at any time
    # activates key once valid from is reached


class Key(BaseModel):
    applications: List[
        ApplicationsKey
    ]  # one key can give access to mulitple appps
    banned: bool

    # NOTE: add bind to user (only specific users can use this key)


class KeyDB(BaseModel):
    bubble_id: str
    bubble_name: str
    keys: Dict[str, Key]
