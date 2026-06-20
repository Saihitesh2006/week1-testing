from typing import Optional

from sqlmodel import Field, SQLModel


class CreditUnion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    charter_number: str
    legal_name: str
    state: str
    asset_band: str
    market: str = ""
    status: str = "verified"


class AppUser(SQLModel, table=True):
    __tablename__ = "app_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    credit_union_id: int = Field(foreign_key="creditunion.id")
    email: str
    is_active: bool = True


class SupportCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str
    label: str
