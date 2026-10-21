SELECT
  id,
  (latitude / 100000) AS latitude,
  (longitude / 100000) AS longitude,
  cp,
  adresse,
  ville,
  prix_Gazole,
  prix_SP95,
  prix_E85,
  prix_GPLc,
  prix_E10,
  prix_SP98,
  carburants_disponibles

FROM {{ ref('stg_fuels_stations_data') }}