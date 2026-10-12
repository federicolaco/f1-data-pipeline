# F1 Data Pipeline

End-to-end data pipeline for Formula 1 data (portfolio project for an entry-level Data Engineer role).

**Stack (target):** Jolpica API → Python/Pandas → PostgreSQL → Apache Airflow → Docker Compose

## Status

In progress. The 2024 season loads from the Jolpica API into staging and analytics. A pytest run fails if the data quality checks return any rows.

## How to run

First, create and activate the virtual environment, and install libraries:

```bash
python -m venv .venv

# Make sure to run the command corresponding to your OS
source .venv/Scripts/activate # Windows Git Bash
source .venv/bin/activate     # macOS and Linux

pip install -r requirements.txt
```

Make sure to have docker running and execute:

```bash
docker compose up -d

python -m src.extract.jolpica_client
python -m src.load.postgres_loader

# Fail if the quality checks return rows, then print the 2024 standings
python -m pytest tests/test_checks.py
docker compose exec -T postgres psql -U f1 -d f1 < sql/04_driver_standings.sql
```
