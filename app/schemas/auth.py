from pydantic import BaseModel

class AdminCreate(BaseModel):
    login: str
    password: str
    role: str

class AdminLogin(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    login: str | None = None
    role: str | None = None