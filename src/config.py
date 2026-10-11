from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

BASE_URL = "https://api.jolpi.ca/ergast/f1"
SEASON = os.getenv("SEASON", "2024")
USER_AGENT = os.getenv("USER_AGENT", "f1-data-pipeline/0.1")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://f1:f1@localhost:5432/f1")
