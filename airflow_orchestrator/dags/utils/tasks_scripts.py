import os
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv
from airflow.exceptions import AirflowException

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/parquet"
PIPELINE_INPUTS_DIR = os.environ["PIPELINE_INPUTS_DIR"]


def api_get_stations():
    print('URL PIPE INPUTS', PIPELINE_INPUTS_DIR)
    try:
        response = requests.get(URL)
        if (response.status_code == 200):
            df = pd.read_parquet(URL)
            print('OK TOUT BON')
            df.to_parquet(f"{PIPELINE_INPUTS_DIR}/raw_fuels_stations.parquet")
        else:
            raise AirflowException(f"STATUS CODE :{response.status_code}")
    except Exception as e:
        print(f"❌ PROBLEME DETECTE: {e}")
        raise
