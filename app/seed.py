import csv
from pathlib import Path

from sqlmodel import Session, select

from app.database import engine, init_db
from app.models import CreditUnion, SupportCategory

CATEGORIES = [
    ("liquidity", "Liquidity"),
    ("loan_participation", "Loan Participation"),
    ("short_term_expert", "Short-Term Expert"),
    ("interim_exec", "Interim Executive"),
    ("shared_space", "Shared Space"),
    ("mentorship", "Mentorship"),
]

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
# Fictional CU roster provided by Ira (PM). See also:
# data/Consortium - Credit Unions - Sheet1.csv
CSV_PATH = DATA_DIR / "fake_credit_unions.csv"


def seed_categories(session: Session) -> None:
    existing = {category.key for category in session.exec(select(SupportCategory)).all()}
    for key, label in CATEGORIES:
        if key not in existing:
            session.add(SupportCategory(key=key, label=label))


def seed_credit_unions(session: Session) -> None:
    if session.exec(select(CreditUnion)).first():
        return

    with CSV_PATH.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not row.get("charter_number", "").strip():
                continue
            session.add(
                CreditUnion(
                    charter_number=row["charter_number"].strip(),
                    legal_name=row["legal_name"].strip(),
                    state=row["state"].strip(),
                    asset_band=row["asset_band"].strip(),
                    market=row.get("market", "").strip(),
                    status="verified",
                )
            )


def seed() -> None:
    init_db()
    with Session(engine) as session:
        seed_categories(session)
        seed_credit_unions(session)
        session.commit()


if __name__ == "__main__":
    seed()
