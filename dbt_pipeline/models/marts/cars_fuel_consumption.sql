SELECT
  brand,
  car_model,
  engine_model,
  CAST(REPLACE(conso_fuel_liter_per_100km,'/','') AS DECIMAL(10,1)) AS conso_fuel_liter_per_100km
FROM {{ ref('int_cars_fuel_consumption_data') }}
WHERE engine_model NOT LIKE '%Electrique' AND conso_fuel_liter_per_100km != ''