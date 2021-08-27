import streamlit as st
import pydeck as pdk
from pydeck.types import String

def generate_pydeck_chart(midpoint, sensor_locations, selected_sensor_locations):
    # try to add either polygon or icon layer to show the floors
    point_layer = (
        pdk.Layer(
            "ScatterplotLayer",
            data=sensor_locations,
            get_position="[lon, lat, height]",
            get_radius=0.5,
        ),
    )

    text_layer = pdk.Layer(
        "TextLayer",
        data=sensor_locations,
        pickable=False,
        get_position="[lon, lat, height]",
        get_text="name",
        get_size=16,
        get_color=[0, 0, 0],
        get_angle=0,
        # can be start, middle, end
        get_text_anchor=String("start"),
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

def render(midpoint, sensor_locations, selected_sensor_locations):
    chart = generate_pydeck_chart(midpoint, sensor_locations, selected_sensor_locations)
    st.pydeck_chart(chart)
