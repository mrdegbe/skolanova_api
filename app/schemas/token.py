# ✅ Because I have a Token response schema

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
