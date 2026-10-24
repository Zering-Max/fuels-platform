import os
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from cosmos import DbtTaskGroup, ExecutionConfig, ProfileConfig, ProjectConfig
from dotenv import load_dotenv
from utils.tasks_scripts import api_get_stations

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

DBT_DIR = os.environ["DBT_PROJECT_DIR"]
DBT_BIN = os.environ["DBT_BIN"]

profile_config = ProfileConfig(
 profile_name="dbt_pipeline",
 target_name="prod",
 profiles_yml_filepath=os.path.join(DBT_DIR, "profiles.yml"),
)

with DAG("ingest_and_build_data",
         start_date=datetime(2026, 10, 19),
         schedule="*/15 * * * *",
         catchup=False,
         tags=["dbt"],
    ) as dag:
    get_data = PythonOperator(
        task_id="api_get_data",
        python_callable=api_get_stations,
        retries=3,
        retry_delay=timedelta(minutes=1),
    )
    dbt_build_data = DbtTaskGroup(
        project_config=ProjectConfig(
            dbt_project_path=DBT_DIR,
        ),
        profile_config=profile_config,
        execution_config=ExecutionConfig(
            dbt_executable_path=DBT_BIN,
        )
    )
    get_data >> dbt_build_data