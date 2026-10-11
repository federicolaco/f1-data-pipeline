import json
import psycopg
from src.config import DATABASE_URL, RAW_DIR, SEASON

def load_drivers() -> None:
  path = RAW_DIR / f"drivers_{SEASON}.json"
  payload = json.loads(path.read_text(encoding = "utf-8"))
  drivers = payload["MRData"]["DriverTable"]["Drivers"]

  rows = [
    (
      driver["driverId"],
      driver.get("code"),
      driver.get("givenName"),
      driver.get("familyName"),
      driver.get("dateOfBirth"),
      driver.get("nationality"),
      driver.get("permanentNumber"),
    ) 
    for driver in drivers
  ]

  sql = """
    INSERT INTO staging.drivers (
      driver_id,
      code,
      given_name,
      family_name,
      date_of_birth,
      nationality,
      permanent_number
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (driver_id) DO UPDATE SET 
      code = EXCLUDED.code, 
      given_name = EXCLUDED.given_name,
      family_name = EXCLUDED.family_name, 
      date_of_birth = EXCLUDED.date_of_birth, 
      nationality = EXCLUDED.nationality, 
      permanent_number = EXCLUDED.permanent_number
  """

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
      cursor.executemany(sql, rows)
  print(f"Loaded {len(rows)} drivers")

def load_constructors() -> None:
  path = RAW_DIR / f"constructors_{SEASON}.json"
  payload = json.loads(path.read_text(encoding="utf-8"))
  constructors = payload["MRData"]["ConstructorTable"]["Constructors"]

  rows = [
    (
      constructor["constructorId"],
      constructor.get("name"),
      constructor.get("nationality"),
    )
    for constructor in constructors
  ]

  sql = """
    INSERT INTO staging.constructors (
      constructor_id, name, nationality
    ) VALUES (%s, %s, %s)
    ON CONFLICT (constructor_id) DO UPDATE SET
      name = EXCLUDED.name,
      nationality = EXCLUDED.nationality
  """

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
      cursor.executemany(sql, rows)
  print(f"Loaded {len(rows)} constructors")

def load_circuits() -> None:
  path = RAW_DIR / f"circuits_{SEASON}.json"
  payload = json.loads(path.read_text(encoding="utf-8"))
  circuits = payload["MRData"]["CircuitTable"]["Circuits"]

  rows = []
  for circuit in circuits:
    location = circuit["Location"]
    rows.append(
      (
        circuit["circuitId"],
        circuit.get("circuitName"),
        location.get("locality"),
        location.get("country"),
        float(location["lat"]),
        float(location["long"]),
      )
    )

  sql = """
    INSERT INTO staging.circuits (
      circuit_id, circuit_name, locality, country, latitude, longitude
    ) VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (circuit_id) DO UPDATE SET
      circuit_name = EXCLUDED.circuit_name,
      locality = EXCLUDED.locality,
      country = EXCLUDED.country,
      latitude = EXCLUDED.latitude,
      longitude = EXCLUDED.longitude
  """

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
      cursor.executemany(sql, rows)
  print(f"Loaded {len(rows)} circuits")

def load_races() -> None:
  path = RAW_DIR / f"races_{SEASON}.json"
  payload = json.loads(path.read_text(encoding="utf-8"))
  races = payload["MRData"]["RaceTable"]["Races"]

  rows = [
    (
      int(race["season"]),
      int(race["round"]),
      race.get("raceName"),
      race["Circuit"]["circuitId"],
      race.get("date"),
    )
    for race in races
  ]

  sql = """
    INSERT INTO staging.races (
      season, round, race_name, circuit_id, race_date
    ) VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (season, round) DO UPDATE SET
      race_name = EXCLUDED.race_name,
      circuit_id = EXCLUDED.circuit_id,
      race_date = EXCLUDED.race_date
  """

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
      cursor.executemany(sql, rows)
  print(f"Loaded {len(rows)} races")

def load_results() -> None:
  paths = sorted(
    RAW_DIR.glob(f"results_{SEASON}_offset_*.json"),
    key=lambda path: int(path.stem.split("_")[-1]),
  )

  rows = []
  for path in paths:
    payload = json.loads(path.read_text(encoding="utf-8"))
    for race in payload["MRData"]["RaceTable"]["Races"]:
      for result in race["Results"]:
        rows.append(
          (
            int(race["season"]),
            int(race["round"]),
            result["Driver"]["driverId"],
            result["Constructor"]["constructorId"],
            int(result["grid"]),
            int(result["position"]),
            float(result["points"]),
            int(result["laps"]),
            result.get("status"),
          )
        )

  sql = """
    INSERT INTO staging.results (
      season, round, driver_id, constructor_id,
      grid, position, points, laps, status
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (season, round, driver_id) DO UPDATE SET
      constructor_id = EXCLUDED.constructor_id,
      grid = EXCLUDED.grid,
      position = EXCLUDED.position,
      points = EXCLUDED.points,
      laps = EXCLUDED.laps,
      status = EXCLUDED.status
  """

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
      cursor.executemany(sql, rows)
  print(f"Loaded {len(rows)} results")

def load_dim_drivers():
  sql = """
    INSERT INTO analytics.dim_drivers (
      driver_id, code, given_name, family_name,
      date_of_birth, nationality, permanent_number
    )
    SELECT
      driver_id, code, given_name, family_name,
      date_of_birth, nationality, permanent_number
    FROM staging.drivers
    ON CONFLICT (driver_id) DO UPDATE SET
      code = EXCLUDED.code,
      given_name = EXCLUDED.given_name,
      family_name = EXCLUDED.family_name,
      date_of_birth = EXCLUDED.date_of_birth,
      nationality = EXCLUDED.nationality,
      permanent_number = EXCLUDED.permanent_number
  """

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
      cursor.execute(sql)
  print("Loaded analytics.dim_drivers")

def load_dim_constructors():
  sql = """
    INSERT INTO analytics.dim_constructors (
      constructor_id, name, nationality
    )
    SELECT
      constructor_id, name, nationality
    FROM staging.constructors
    ON CONFLICT (constructor_id) DO UPDATE SET 
      name = EXCLUDED.name,
      nationality = EXCLUDED.nationality
  """

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
      cursor.execute(sql)
  print("Loaded analytics.dim_constructors")

def load_dim_circuits():
  sql = """
    INSERT INTO analytics.dim_circuits (
      circuit_id, circuit_name, locality, country, latitude, longitude
    ) 
    SELECT 
      circuit_id, circuit_name, locality, country, latitude, longitude
    FROM staging.circuits
    ON CONFLICT (circuit_id) DO UPDATE SET
      circuit_name = EXCLUDED.circuit_name,
      locality = EXCLUDED.locality,
      country = EXCLUDED.country,
      latitude = EXCLUDED.latitude,
      longitude = EXCLUDED.longitude
  """

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
      cursor.execute(sql)
    print("Loaded analytics.dim_circuits")

def load_dim_races():
  sql = """
    INSERT INTO analytics.dim_races (
      season, round, race_name, circuit_id, race_date
    ) 
    SELECT 
      season, round, race_name, circuit_id, race_date
    FROM staging.races
    ON CONFLICT (season, round) DO UPDATE SET
      race_name = EXCLUDED.race_name,
      circuit_id = EXCLUDED.circuit_id,
      race_date = EXCLUDED.race_date
  """

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
      cursor.execute(sql)
    print("Loaded analytics.dim_races")

def load_fact_results():
  sql = """
    INSERT INTO analytics.fact_results (
      season, round, driver_id, constructor_id,
      grid, position, points, laps, status
    )
    SELECT
      season, round, driver_id, constructor_id,
      grid, position, points, laps, status
    FROM staging.results
    ON CONFLICT (season, round, driver_id) DO UPDATE SET
      constructor_id = EXCLUDED.constructor_id,
      grid = EXCLUDED.grid,
      position = EXCLUDED.position,
      points = EXCLUDED.points,
      laps = EXCLUDED.laps,
      status = EXCLUDED.status
  """

  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
      cursor.execute(sql)
    print("Loaded analytics.fact_results")

if __name__ == "__main__":
  load_drivers()
  load_constructors()
  load_circuits()
  load_races()
  load_results()
  load_dim_drivers()
  load_dim_constructors()
  load_dim_circuits()
  load_dim_races()
  load_fact_results()