from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime



class TokenBase(SQLModel):
    """
    Tokenbase model for Token.

    Attributes:
        user_id (int):
        access_token (int): 
        refresh_token
        expires_at: 
    """
    user_id: int  # Name of the token
    access_token: str  # Description of the token
    refresh_token: str
    expires_at: datetime


class Token(TokenBase, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True)  # Primary key for token


class TokenCreate(TokenBase):
    pass