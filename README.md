# CU Consortium MVP

A confidential, credit-union-only mutual-aid prototype. Small CUs anonymously request help; large CUs browse and offer support; identities reveal only after two-party consent.

**Stack:** FastAPI, SQLModel, PostgreSQL, Jinja2, Tailwind CSS

## Prerequisites

- Python 3.12
- PostgreSQL 16 (or Docker)

## Setup

1. Clone the repository and enter the project directory:

   ```bash
   git clone <repo-url>
   cd consortium
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS/Linux
   ```

   **Windows PowerShell note:** If `activate` fails with an execution policy error, either run this once in PowerShell (current user only):

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   Or skip activation and call tools directly:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database connection:

   ```bash
   copy .env.example .env        # Windows
   cp .env.example .env          # macOS/Linux
   ```

   Edit `.env` and set `DATABASE_URL`:

   ```
   DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/consortium
   ```

5. Create the PostgreSQL database (if it does not exist):

   ```bash
   createdb consortium
   ```

   Or with Docker:

   ```bash
   docker run --name consortium-db -e POSTGRES_PASSWORD=consortium -e POSTGRES_DB=consortium -p 5432:5432 -d postgres:16
   ```

6. Load seed data:

   ```bash
   python -m app.seed
   ```

7. Run the app:

   ```bash
   uvicorn app.main:app --reload
   ```

8. Open in browser:

   - Landing page: http://127.0.0.1:8000/
   - Health check: http://127.0.0.1:8000/health
   - Dashboard stub: http://127.0.0.1:8000/dashboard

## Verify seed data

```bash
psql -d consortium -c "SELECT legal_name, state FROM creditunion;"
psql -d consortium -c "SELECT key, label FROM supportcategory;"
psql -d consortium -c "\dt"
```

Fictional CU roster is provided by Ira (PM) in `data/Consortium - Credit Unions - Sheet1.csv`.

**Note:** The user table was renamed to `app_user` because `user` is a reserved word in PostgreSQL. If you cloned an older version that still has a `user` table, run:

```bash
psql -d consortium -f scripts/drop_user_table.sql
python -c "from app.database import init_db; import app.models; init_db()"
```

## Week 1 scope

- App skeleton with `/health` and landing page
- PostgreSQL connected with three core tables (`creditunion`, `app_user`, `supportcategory`)
- Seed data: 20 fictional credit unions from Ira (PM) and 6 support categories
- Responsive landing page styled with Tailwind

**Not in Week 1:** deployment, verification logic, sign-in, or feature screens.

## Team

| Person | Role |
| ------ | ---- |
| Sai + Gaurav | Backend + Frontend |
| Ira | Product / PM |
| Mehak | Design / QA |

The Week 1 demo follows the four-person run-of-show: Ira opens and closes, Mehak presents Figma, Sai and Gaurav run the live app and database query.

## Data rule

Use fictional credit unions and fake people only. Never commit real CU or member data.
