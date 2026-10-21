FROM apache/airflow:3.1.0-python3.12
# 1) Airflow + astronomer-cosmos dans l'env principal, verrouillés par les constraints
RUN pip install --no-cache-dir \
"apache-airflow==3.1.0" \
--constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.12.txt" \
astronomer-cosmos \
pandas \
pyarrow \
requests \
# 2) dbt dans un venv séparé : AUCUNE dépendance partagée avec Airflow
RUN python -m venv /home/airflow/dbt_venv \
&& /home/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-duckdb
# exécutable pointé explicitement par le DAG
ENV DBT_BIN=/home/airflow/dbt_venv/bin/dbt