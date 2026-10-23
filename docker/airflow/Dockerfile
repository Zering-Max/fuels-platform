FROM apache/airflow:3.1.0-python3.12
# Airflow + astronomer-cosmos (for a good overview of DBT in airflow), pandas, pyarrow and request because of API requests and parquet table creation
RUN pip install --no-cache-dir \
"apache-airflow==3.1.0" \
--constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.12.txt" \
astronomer-cosmos \
pandas \
pyarrow \
requests
# DBT project created in a venv isolated from airflow venv (prevent dependences incompatibilities)
RUN python -m venv /home/airflow/dbt_venv \
&& /home/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-duckdb
# environment variable for DAG
ENV DBT_BIN=/home/airflow/dbt_venv/bin/dbt