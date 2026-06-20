import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()

_raw_url = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:consortium@localhost:5432/consortium",
)
if _raw_url.startswith("postgres://"):
    _raw_url = _raw_url.replace("postgres://", "postgresql+psycopg://", 1)

DATABASE_URL = _raw_url

engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
