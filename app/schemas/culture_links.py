from typing import Optional
from pydantic import BaseModel

class ConnectedArticleCreate(BaseModel):
    linked_article_id: int

class ConnectedArticleResponse(BaseModel):
    id: int
    id_culture: int
    linked_article_id: int

    class Config:
        from_attributes = True

class LinkedArticleInfo(BaseModel):
    id: int
    title: str
    region: Optional[str]
    main_photo: Optional[str]

    class Config:
        from_attributes = True