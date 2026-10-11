from src.config import PROJECT_ROOT, DATABASE_URL
import psycopg

def  test_checks_return_no_rows():
  sql = (PROJECT_ROOT / "sql" / "03_checks.sql").read_text(encoding="utf-8")
  statements = [piece.strip() for piece in sql.split(";") if piece.strip()]

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
      for statement in statements:
        cursor.execute(statement)
        assert cursor.fetchall() == []