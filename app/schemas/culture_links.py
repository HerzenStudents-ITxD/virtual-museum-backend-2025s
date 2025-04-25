from typing import Optional
from pydantic import BaseModel

class ConnectedArticleBase(BaseModel):
    linked_article_id: int
    id_culture: int

class ConnectedArticleCreate(ConnectedArticleBase):
    pass

class ConnectedArticleResponse(ConnectedArticleBase):
    id: int

    class Config:
        from_attributes = True

#!!!!!подумать над этим!!!!
class LinkedArticleInfo(BaseModel):
    id: int
    title: str
    main_photo: Optional[str]