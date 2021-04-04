""" Data models module. """
from typing import List
from pydantic import BaseModel, Field
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .models import User, UserReceipt

PydanticUser = sqlalchemy_to_pydantic(User)
PydanticReceipt = sqlalchemy_to_pydantic(UserReceipt)


class PydanticUserWithReceipts(PydanticUser):
    user_data: List[PydanticReceipt] = []


class ReceiptBody(BaseModel):
    receipt_data: bytes = Field(alias='receipt-data')
    exclude_transactions: bool = Field(alias='exclude-old-transactions')
    sandbox: bool
    password: str
