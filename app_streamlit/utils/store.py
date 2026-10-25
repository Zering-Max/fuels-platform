import streamlit as st
from app_streamlit.utils.constantes import (
    BRAND,
    CAR_MODEL,
    ENGINE_MODEL,
    FUEL_TYPE,
    PERSON_ADDRESS,
    QUANTITY,
    RADIUS,
)
from pandas import DataFrame

session_conditions = (
  PERSON_ADDRESS
  and RADIUS
  and FUEL_TYPE
  and QUANTITY
  and BRAND
  and CAR_MODEL
  and ENGINE_MODEL
)

def trigger_map(
    address_value:str,
    radius_value:int,
    fuel_value:str,
    quantity_value:int,
    brand_value:str,
    car_model_value:str,
    engine_model_value:str
):
  st.session_state[PERSON_ADDRESS] = address_value
  st.session_state[RADIUS] = radius_value
  st.session_state[FUEL_TYPE] = fuel_value
  st.session_state[QUANTITY] = quantity_value
  st.session_state[BRAND] = brand_value
  st.session_state[CAR_MODEL] = car_model_value
  st.session_state[ENGINE_MODEL] = engine_model_value