CREATE TABLE IF NOT EXISTS analytics.dim_drivers (
  driver_id TEXT PRIMARY KEY,
  code TEXT,
  given_name TEXT,
  family_name TEXT,
  date_of_birth DATE,
  nationality TEXT,
  permanent_number TEXT
);

CREATE TABLE IF NOT EXISTS analytics.dim_constructors (
  constructor_id TEXT PRIMARY KEY,
  name TEXT,
  nationality TEXT
);

CREATE TABLE IF NOT EXISTS analytics.dim_circuits (
  circuit_id TEXT PRIMARY KEY,
  circuit_name TEXT,
  locality TEXT,
  country TEXT,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS analytics.dim_races (
  season INTEGER NOT NULL,
  round INTEGER NOT NULL,
  race_name TEXT,
  circuit_id TEXT,
  race_date DATE,
  PRIMARY KEY (season, round),
  CONSTRAINT fk_dim_races_circuit
    FOREIGN KEY (circuit_id) REFERENCES analytics.dim_circuits (circuit_id)
);

CREATE TABLE IF NOT EXISTS analytics.fact_results (
  season INTEGER NOT NULL,
  round INTEGER NOT NULL,
  driver_id TEXT NOT NULL,
  constructor_id TEXT,
  grid INTEGER,
  position INTEGER,
  points NUMERIC,
  laps INTEGER,
  status TEXT,
  PRIMARY KEY (season, round, driver_id),
  CONSTRAINT fk_fact_results_driver
    FOREIGN KEY (driver_id) REFERENCES analytics.dim_drivers (driver_id),
  CONSTRAINT fk_fact_results_constructor
    FOREIGN KEY (constructor_id) REFERENCES analytics.dim_constructors (constructor_id),
  CONSTRAINT fk_fact_results_race
    FOREIGN KEY (season, round) REFERENCES analytics.dim_races (season, round)
);