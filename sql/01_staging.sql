CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS staging.drivers (
    driver_id TEXT PRIMARY KEY,
    code TEXT,
    given_name TEXT,
    family_name TEXT,
    date_of_birth DATE,
    nationality TEXT,
    permanent_number TEXT
);

CREATE TABLE IF NOT EXISTS staging.constructors (
    constructor_id TEXT PRIMARY KEY,
    name TEXT,
    nationality TEXT
);

CREATE TABLE IF NOT EXISTS staging.circuits (
    circuit_id TEXT PRIMARY KEY,
    circuit_name TEXT,
    locality TEXT,
    country TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS staging.races (
    season INTEGER NOT NULL,
    round INTEGER NOT NULL,
    race_name TEXT,
    circuit_id TEXT,
    race_date DATE,
    PRIMARY KEY (season, round)
);

CREATE TABLE IF NOT EXISTS staging.results (
    season INTEGER NOT NULL,
    round INTEGER NOT NULL,
    driver_id TEXT NOT NULL,
    constructor_id TEXT,
    grid INTEGER,
    position INTEGER,
    points NUMERIC,
    laps INTEGER,
    status TEXT,
    PRIMARY KEY (season, round, driver_id)
);