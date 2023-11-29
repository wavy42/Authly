from typing import Optional
from pydantic import BaseModel


class BubbleSettings(BaseModel):
    allow_new_user_registration: Optional[bool] = True
    test_settings: Optional[str] = "HelloWorld"
    bliblablu: Optional[bool] = True


class BubbleConfig(BaseModel):
    id: Optional[str] = None
    name: str
    settings: BubbleSettings

    # NOTE: dict with the collection name and the object id of the document:
    user_document_id: Optional[str] = None
    key_document_id: Optional[str] = None
    application_document_id: Optional[str] = None


class CreateBubble(BaseModel):
    name: str
    settings: BubbleSettings
