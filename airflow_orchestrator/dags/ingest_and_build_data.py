import os
from airflow import DAG
from datetime import datetime, timedelta
from utils.tasks_scripts import api_get_stations
from airflow.operators.python import PythonOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig

DBT_DIR = os.environ["DBT_PROJECT_DIR"]
DBT_BIN = os.environ["DBT_BIN"]

profile_config = ProfileConfig(
 profile_name="default",
 target_name="prod",
 profiles_yml_filepath=os.path.join(DBT_DIR, "profiles.yml"),
)

with DAG("ingest_and_build_data",
         start_date=datetime(2026, 10, 19),
         schedule="0 0,3,6,9,12,15,18,21 * * *",
         catchup=False,
         tags=["dbt"],
    ) as dag:
    get_data = PythonOperator(
        task_id="api_get_data",
        python_callable=api_get_stations,
        retries=3,
        retry_delay=timedelta(minutes=5),
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