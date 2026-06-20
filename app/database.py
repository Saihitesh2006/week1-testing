import os
from typing import Optional

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from sqlalchemy.engine import Engine

load_dotenv()


def normalize_database_url(raw_url: str) -> Optional[str]:
    url = raw_url.strip()
    if not url or url.lower() in {"none", "null", "undefined"}:
        return None
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://") and "+psycopg" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    if not url.startswith("postgresql"):
        return None
    return url


def resolve_database_url() -> Optional[str]:
    configured = normalize_database_url(os.environ.get("DATABASE_URL", ""))
    if configured:
        return configured

    # Week 1 landing-only deploys do not require a database.
    if os.environ.get("PORT"):
        return None

    return normalize_database_url(
        "postgresql+psycopg://saihitesh@localhost:5432/consortium"
    )


DATABASE_URL = resolve_database_url()
engine: Engine | None = (
    create_engine(DATABASE_URL, echo=False) if DATABASE_URL else None
)


def init_db() -> None:
    if engine is None:
        return
    SQLModel.metadata.create_all(engine)
