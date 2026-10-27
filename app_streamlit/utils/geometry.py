from geopy.geocoders import Nominatim
from pandas import DataFrame
from shapely.geometry import Point
import geopandas as gpd
from typing import List

def calculate_lat_lon_address(person_address:str):
  app_geo = Nominatim(user_agent="tutorial")
  try:
    location = app_geo.geocode(person_address).raw

    lat_center = float(location["lat"])
    lon_center = float(location["lon"])
    return [lat_center, lon_center]
  except Exception as e:
    print(f"❌ Échec : {e}")
    return 'error'

def get_fuel_stations_in_radius(df:DataFrame,coord_center:List[float] ,radius:int, type_fuel:str) -> DataFrame:
  radius_m = radius * 1000

  # Créer un GeoDataFrame à partir du DataFrame
  geometry = [Point(xy) for xy in zip(df['latitude'], df['longitude'])]
  # EPSG 4326 pour stocker les données géo, sinon en web app on passe en 3857 (les coordonnées sont alors convertis en mètres)
  gdf_adresses = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
  gdf_adresses = gdf_adresses.to_crs(epsg=3857)  # Projection Web Mercator

  # Créer un point central en géométrie
  center = Point(coord_center[0], coord_center[1])
  gdf_center = gpd.GeoDataFrame(geometry=[center], crs="EPSG:4326")
  gdf_center = gdf_center.to_crs(epsg=3857)

  # Calculer la distance entre chaque point et le centre
  gdf_adresses['distance_m'] = gdf_adresses.geometry.distance(gdf_center.geometry[0])

  # Filtrer les adresses à l'intérieur du cercle
  df_filtered = gdf_adresses[(gdf_adresses['distance_m'] <= radius_m)&(gdf_adresses['carburants_disponibles'].str.contains(type_fuel))]
  return df_filtered


def get_top5_stations(
    df_stations:DataFrame,
    df_conso_cars_fuel:DataFrame,
    quantity:int,
    fuel_type:str,
    brand:str,
    car_model:str,
    engine_model:str
) -> DataFrame:
  map_data = df_stations[["latitude", "longitude", "adresse", "cp", "ville",
        f"prix_{fuel_type}", "distance_m"]]
  map_data["distance_m"] = round(map_data["distance_m"] / 1000, 1)
  map_data["max_price"] = round(map_data[f"prix_{fuel_type}"].max(),3)
  conso_car = df_conso_cars_fuel[(df_conso_cars_fuel["brand"]==brand)&(df_conso_cars_fuel["car_model"]==car_model)&(df_conso_cars_fuel["engine_model"]==engine_model)]["conso_fuel_liter_per_100km"].values[0]

  map_data["money_discount"] = round((map_data["max_price"] - map_data[f"prix_{fuel_type}"]) * (quantity - ((conso_car / 100) * map_data["distance_m"])),1)
  result = map_data.sort_values(by=["money_discount", "distance_m"], ascending=[False, True]).head(5)
  return result