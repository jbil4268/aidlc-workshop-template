from pydantic import BaseModel


class TableLoginRequest(BaseModel):
    qr_code: str


class TableLoginResponse(BaseModel):
    session_token: str
    table_number: str
    table_id: int


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
