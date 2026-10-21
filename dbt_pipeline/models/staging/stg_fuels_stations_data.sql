SELECT
  CAST("id" AS VARCHAR) AS id,
  CAST("latitude" AS FLOAT) AS latitude,
  CAST("longitude" AS FLOAT) AS longitude,
  cp,
  adresse,
  ville,
  CAST("gazole_prix" AS FLOAT) AS prix_Gazole,
  CAST("sp95_prix" AS FLOAT) AS prix_SP95,
  CAST("e85_prix" AS FLOAT) AS prix_E85,
  CAST("gplc_prix" AS FLOAT) AS prix_GPLc,
  CAST("e10_prix" AS FLOAT) AS prix_E10,
  CAST("sp98_prix" AS FLOAT) AS prix_SP98,
  carburants_disponibles,
  departement,
  code_departement,
  region,
  code_region

FROM '{{ env_var('PIPELINE_INPUTS_DIR') }}/raw_fuels_stations.parquet'
