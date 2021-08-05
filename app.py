import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
from pydeck.types import String

# streamlit run app.py
# https://share.streamlit.io/daanduppen/sensor-data-demo-app/main/app.py

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


def get_midpoint():
    return {"lat": 52.3671182, "lon": 4.9038155}


def get_sensor_locations():
    sensor_locations = pd.read_csv("data/sensor_locations.csv")
    sensor_locations = sensor_locations.round(6)
    return sensor_locations


def get_sensor_data(sensor_name):
    sensor_data = pd.read_csv(f"data/vorigemaand_clean_sensor_{sensor_name}.csv", index_col=0)
    sensor_data.date = pd.to_datetime(sensor_data.date, format="%Y%m%d %H")
    return sensor_data


def get_pydeck_chart(midpoint, sensor_locations):
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
        data=sensor_locations,
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

    sensor_pydeck_chart = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=initial_view_state,
        layers=[point_layer, text_layer],
    )
    return sensor_pydeck_chart


def get_sensor_dropdown(sensor_locations):
    selection_options = pd.Series(["all"]).append(sensor_locations["name"])
    return selection_options

sensor_name = '1-1'

# data

midpoint = get_midpoint()
sensor_locations = get_sensor_locations()
sensor_data = get_sensor_data(sensor_name)

# components
sensor_pydeck_chart = get_pydeck_chart(midpoint, sensor_locations)
selection_options = get_sensor_dropdown(sensor_locations)

# page
st.title("Sensor dashboard")
# sensor_locations
st.pydeck_chart(sensor_pydeck_chart)
selection = st.selectbox("Choose point ID", selection_options)


# sensor_data.loc[:,['index', 'T']]
d = {'hour': sensor_data.date.dt.hour, 'week': sensor_data.date.dt.week}
# df.groupby([df.date.dt.month, df.date.dt.day]).temperature.mean().to_frame()
# sensor_data = sensor_data.groupby([sensor_data.date.dt.hour]).temperature.mean().to_frame()
# df.groupby([df.date.dt.day]).temperature.mean().to_frame()
# df.groupby([df.date.dt.hour]).temperature.mean().to_frame()

'sensor 1-1'
start_date = st.date_input('start_date', value=sensor_data.date.min(), min_value=sensor_data.date.min(), max_value=sensor_data.date.max())
end_date = st.date_input('end_date', value=sensor_data.date.max(), min_value=sensor_data.date.min(), max_value=sensor_data.date.max())
sensor_data = sensor_data.set_index("date")
# sensor_data = sensor_data.iloc[0:25]
selected_date_range = sensor_data["temperature"].loc[start_date: end_date]
st.line_chart(selected_date_range)