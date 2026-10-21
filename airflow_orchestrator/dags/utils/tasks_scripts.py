import os
from typing import Dict, List
import pandas as pd
import requests
from airflow.exceptions import AirflowException


URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/parquet"
PIPELINE_INPUTS_DIR = os.environ["PIPELINE_INPUTS_DIR"]


def api_get_stations():
    response = requests.get(URL)

    try:
        if (response.status_code == 200):
            df = pd.read_parquet(URL)
            df.to_parquet(f"{PIPELINE_INPUTS_DIR}/raw_fuels_stations.parquet")
        else:
            raise AirflowException(f"STATUS CODE :{response.status_code}")
    except Exception as e:
        print(f"❌ PROBLEME DETECTE: {e}")
        raise
