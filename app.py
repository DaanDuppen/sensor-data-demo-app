import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
from pydeck.types import String

# streamlit run first_app.py

# Done
# text alignment
# sensor data
# graph

# add
# graphs
# sensor selection
# singular graph
# host
# 3D walls? areas?
# levels
# tooltip for each dot


def get_sensor_locations():
    sensor_locations = pd.read_csv('data/sensor_locations.csv')
    sensor_locations = sensor_locations.round(6)
    return sensor_locations




def generate_sensor_map(midpoint, sensor_locations):
    point_layer = (
    pdk.Layer(
        "ScatterplotLayer",
        data=sensor_locations,
        get_position="[lon, lat]",
        get_radius=0.5,
    ),
)

    text_layer = pdk.Layer(
    "TextLayer",
    sensor_locations,
    pickable=True,
    get_position="[lon, lat]",
    get_text="name",
    get_size=16,
    get_color=[0, 0, 0],
    get_angle=0,
    get_text_anchor=String("middle"),
    # can be center, bottom, top
    get_alignment_baseline=String("bottom"),
)

    initial_view_state = pdk.ViewState(
            latitude=midpoint["lat"],
            longitude=midpoint["lon"],
            zoom=18,
            pitch=50,
        )

    st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=initial_view_state,
        layers=[point_layer, text_layer],
    )
)



# data
midpoint = {"lat": 52.3671182, "lon": 4.9038155}
sensor_locations = get_sensor_locations()
selection_options = pd.Series(['all']).append(sensor_locations['name'])
sensor_data = pd.read_csv('data/vorigemaand_clean.csv', index_col=0)

# page
st.title("Sensor dashboard")
# sensor_locations

generate_sensor_map(midpoint, sensor_locations)
selection = st.selectbox("Choose point ID", selection_options)

# sensor_data.loc[:,['date', 'T']]
df = sensor_data.set_index('date')
df = df.iloc[0:25]
st.line_chart(df['T'])
