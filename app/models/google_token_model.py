from typing import Optional
from sqlmodel import SQLModel, Field # type: ignore
from datetime import datetime



class TokenBase(SQLModel):
    """
    Tokenbase model for Token.

    Attributes:
        email (int):
        access_token (int): 
        refresh_token
        expires_at: 
    """
    email: str
    access_token: str 
    refresh_token: str
    expires_at: int


class Token(TokenBase, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True)  # Primary key for token


class TokenCreate(TokenBase):
    pass