SELECT
  brand,
  car_model,
  engine_model,
  REPLACE(conso_fuel_liter_per_100km,' litres','') AS conso_fuel_liter_per_100km
FROM '{{ env_var('PIPELINE_INPUTS_DIR') }}/raw_cars_fuel_consumption.parquet'
WHERE engine_model != ''