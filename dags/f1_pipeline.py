from datetime import datetime
from airflow.decorators import dag, task  # type: ignore[import-not-found]
from src.extract.jolpica_client import main as extract_main
from src.load.postgres_loader import (
    load_circuits,
    load_constructors,
    load_dim_circuits,
    load_dim_constructors,
    load_dim_drivers,
    load_dim_races,
    load_drivers,
    load_fact_results,
    load_races,
    load_results,
)

@dag(start_date=datetime(2026, 10, 1), schedule=None, catchup=False)
def f1_pipeline():
    @task
    def extract():
        extract_main()

    @task
    def load():
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
        
    extract() >> load()

f1_pipeline()