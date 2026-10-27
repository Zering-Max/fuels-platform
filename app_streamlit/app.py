import duckdb
import streamlit as st

from utils.constantes import (
    BRAND,
    CAR_MODEL,
    ENGINE_MODEL,
    FUEL_TYPE,
    OPTIONS_FUEL,
    OPTIONS_RADIUS,
    PERSON_ADDRESS,
    QUANTITY,
    RADIUS,
)
from utils.geometry import (
    calculate_lat_lon_address,
    get_fuel_stations_in_radius,
    get_top5_stations,
)
from utils.store import trigger_map, session_conditions
from utils.plotly import change_zoom, create_map

@st.cache_resource # One connection by process
def cloud_con() -> duckdb.DuckDBPyConnection:
 return duckdb.connect(
    st.secrets["motherduck"]["DATABASE"],
    config={"motherduck_token": st.secrets["motherduck"]["TOKEN"]},
 )

# TTL alignée sur la fréquence du DAG
@st.cache_data(ttl=10800)
def load_table(table: str):
 return cloud_con().sql(f"SELECT * FROM main.{table}").df()

st.title("J'économise pour du carburant ⛽")
st.markdown("Plus besoin de noeuds au cerveau, je te donne les 5 stations où tu peux faire le plus d'économies NETTES (en prenant en compte ta voiture, la distance où se trouve la station, etc..) autour de toi.")
st.divider()

# con = duckdb.connect(database=f"{st.secrets['DUCKDB_TABLE_DEV']}", read_only=True)

df_stations = load_table("fuels_stations")
# df_stations = con.execute("SELECT * FROM main.fuels_stations").df()
df_conso = load_table("cars_fuel_consumption")
# df_conso = con.execute("SELECT * FROM main.cars_fuel_consumption").df()

if session_conditions not in st.session_state:
    st.session_state[PERSON_ADDRESS] = ''
    st.session_state[RADIUS] = 0
    st.session_state[FUEL_TYPE] = ''
    st.session_state[QUANTITY] = 0
    st.session_state[BRAND] = ''
    st.session_state[CAR_MODEL] = ''
    st.session_state[ENGINE_MODEL] = ''

st.markdown("#### Où je suis et quel carburant")

col1, col2 = st.columns(2)

with col1:
    address_value = st.text_input(
        label="Adresse",
        placeholder="Ecris une adresse",
    )

    radius_value = st.selectbox(
        label="Rayon d'action (en km)",
        options=OPTIONS_RADIUS,
        index=None,
        placeholder="distance à vol d'oiseau autour de toi ?",
    )

with col2:
    fuel_value = st.selectbox(
        label="Type de carburant",
        options=OPTIONS_FUEL,
        index=None,
        placeholder="Quel type ?",
    )

    quantity_value = st.number_input(
        "Quantité de carburant (en Litres)",
        step=1, min_value=0, max_value=500,
        format="%0.0f",
        value=0,
        help="Il faut donner une valeur entre 0 et 500."
    )

st.markdown("#### Mon type de voiture")

col3, col4 = st.columns(2)

with col3:
    brand_value = st.selectbox(
        label="Marque de voiture",
        options=df_conso[BRAND].drop_duplicates(),
        index=None,
        placeholder="Quelle marque ?",
    )

with col4:
    car_model_value = st.selectbox(
        label="Modèle de voiture",
        options=df_conso[df_conso[BRAND] == brand_value][CAR_MODEL].drop_duplicates(),
        index=None,
        placeholder="Quel modèle ?",
    )


    engine_model_value = st.selectbox(
        label="Modèle de moteur",
        options=df_conso[(df_conso[BRAND] == brand_value)&(df_conso[CAR_MODEL] == car_model_value)][ENGINE_MODEL].drop_duplicates(),
        index=None,
        placeholder="Quel moteur ?",
    )


st.space(size="medium")
validate_address = st.button(
    label='Je cherche les stations',
    on_click=trigger_map,
    args=(address_value, radius_value, fuel_value,quantity_value,brand_value,car_model_value, engine_model_value, ),
    width="stretch",
    icon="🔎",
    type="primary"
)

if (
    st.session_state[PERSON_ADDRESS] != ''
    and st.session_state[RADIUS] != 0
    and st.session_state[FUEL_TYPE] != ''
    and st.session_state[QUANTITY] != 0
    and st.session_state[BRAND] != ''
    and st.session_state[CAR_MODEL] != ''
    and st.session_state[ENGINE_MODEL] != ''
):
    ## CALCUL GEOMETRIE POINT CENTRAL & FILTRAGE DES ADRESSES SELON LE RAYON d'ACTION

    coord_center = calculate_lat_lon_address(person_address=st.session_state[PERSON_ADDRESS])

    if coord_center != 'error':
        df_filtered = get_fuel_stations_in_radius(
            df=df_stations,
            coord_center=coord_center,
            radius=st.session_state[RADIUS],
            type_fuel=st.session_state[FUEL_TYPE],
        )
        ## GRAPHE MAP

        map_data = get_top5_stations(
            df_stations=df_filtered,
            df_conso_cars_fuel=df_conso,
            quantity=st.session_state[QUANTITY],
            fuel_type=st.session_state[FUEL_TYPE],
            brand=st.session_state[BRAND],
            car_model=st.session_state[CAR_MODEL],
            engine_model=st.session_state[ENGINE_MODEL]
        )

        fig = create_map(df=map_data,coord_center=coord_center, zoom=change_zoom(st.session_state[RADIUS]))
        st.plotly_chart(fig, selection_mode="points")
    else:
        st.error("L'adresse donnée est peut être trop précise, ré-essaye avec une adresse plus globale.", icon="⚠️")
