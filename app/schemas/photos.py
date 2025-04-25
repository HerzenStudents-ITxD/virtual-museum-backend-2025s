from pydantic import BaseModel

class PhotoBase(BaseModel):
    photo: str

class PhotoCreate(PhotoBase):
    pass

class PhotoResponse(PhotoBase):
    id: int
    id_exhibit: int

    class Config:
        from_attributes = True