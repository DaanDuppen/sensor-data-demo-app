import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
from pydeck.types import String
from bokeh.plotting import figure
import altair as alt

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


# sensor 1-1,4.9034616182839414,52.36717646478602,15


def _max_width_():
    max_width_str = f"max-width: 1000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


def get_midpoint():
    return {"lat": 52.3671182, "lon": 4.9038155}
    # return {"lat": 49.196, "lon": -123.0}


def get_sensor_locations():
    sensor_locations = pd.read_csv("data/sensor_locations.csv")
    sensor_locations = sensor_locations.round(8)
    return sensor_locations


def get_multiple_sensor_data(get_singular_sensor_data):
    sensor_dict = {"1-1": None, "1-2": None}
    for sensor_name in sensor_dict.keys():
        sensor_dict[sensor_name] = get_singular_sensor_data(sensor_name)
    return sensor_dict


def get_singular_sensor_data(sensor_name):
    sensor_data = pd.read_csv(
        f"data/vorigemaand_clean_sensor_{sensor_name}.csv", index_col=0
    )
    sensor_data.date = pd.to_datetime(sensor_data.date, format="%Y%m%d %H")
    return sensor_data


def get_min_max_date(sensor_dict):
    sensor_data = sensor_dict["1-1"]
    min_date = sensor_data.date.min()
    max_date = sensor_data.date.max()
    return min_date, max_date


def render_pydeck_chart(midpoint, sensor_locations):
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

    st.pydeck_chart(sensor_pydeck_chart)


def render_sensor_dropdown(sensor_locations):
    selection_options = ["all"] + list(sensor_locations["name"])
    selection = st.sidebar.selectbox("Choose point ID", selection_options)
    return selection


def render_level_dropdown(sensor_locations):
    possible_levels = ["all"] + list(sensor_locations["level"].unique())
    selection = st.sidebar.selectbox("Choose building level", possible_levels)
    return selection


def render_start_date_selection(min_date, max_date):
    start_date = st.sidebar.date_input(
        "start_date",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
    )

    return start_date


def render_end_date_selection(min_date, max_date):
    end_date = st.sidebar.date_input(
        "end_date",
        value=max_date,
        min_value=min_date,
        max_value=max_date,
    )

    return end_date


def render_sensor_type_checkboxes():
    sensor_type_bools = {
        "temperature": True,
        "humidity": True,
        "light_intensity": True,
        "air_pressure": True,
    }
    sensor_type_bools = {
        sensor_type.replace("-", " "): sensor_bool
        for sensor_type, sensor_bool in sensor_type_bools.items()
    }
    for sensor_type, sensor_bool in sensor_type_bools.items():
        sensor_type_bools[sensor_type] = st.sidebar.checkbox(
            sensor_type, value=sensor_bool
        )
    return sensor_type_bools


# def filter_by_dt_property():
#     d = {"hour": sensor_data.date.dt.hour, "week": sensor_data.date.dt.week}
# df.groupby([df.date.dt.month, df.date.dt.day]).temperature.mean().to_frame()
# sensor_data = sensor_data.groupby([sensor_data.date.dt.hour]).temperature.mean().to_frame()
# df.groupby([df.date.dt.day]).temperature.mean().to_frame()
# df.groupby([df.date.dt.hour]).temperature.mean().to_frame()


def render_sidebar_sensor_filters(sensor_locations, min_date, max_date):
    st.sidebar.title("Filter sensors")
    level_selection = render_level_dropdown(sensor_locations)
    sensor_selection = render_sensor_dropdown(sensor_locations)

    st.sidebar.title("Filter dates")
    start_date = render_start_date_selection(min_date, max_date)
    end_date = render_end_date_selection(min_date, max_date)

    st.sidebar.title("Filter sensor types")
    sensor_type_bools = render_sensor_type_checkboxes()

    return level_selection, sensor_selection, sensor_type_bools, start_date, end_date


def render_sensor_list(sensor_dict, start_date, end_date):
    for sensor_name, sensor_data in sensor_dict.items():
        sensor_data = sensor_data.set_index("date")
        selected_date_range = sensor_data.loc[start_date:end_date]

        render_sensor_card(sensor_name, selected_date_range)


def render_sensor_card(sensor_name, selected_date_range):
    chart_settings = {
        "temperature": {
            "title": "Temperature measurements [C]",
            "x_axis_col_name": "date",
            "x_axis_title": "Measurement date",
            "y_axis_col_name": "temperature",
            "y_axis_title": "Temperature",
            "y_axis_format": "C",
        },
        "humidity": {
            "title": "Humidity measurements [%]",
            "x_axis_col_name": "date",
            "x_axis_title": "Measurement date",
            "y_axis_col_name": "humidity",
            "y_axis_title": "Humidity",
            "y_axis_format": "%",    
        },
        "light_intensity": {
            "title": "Light intensity measurements [candela]",
            "x_axis_col_name": "date",
            "x_axis_title": "Measurement date",
            "y_axis_col_name": "light_intensity",
            "y_axis_title": "Light intensity",
            "y_axis_format": "candela",    
        },
        "air_pressure": {
            "title": "air_pressure measurements [atm]",
            "x_axis_col_name": "date",
            "x_axis_title": "Measurement date",
            "y_axis_col_name": "air_pressure",
            "y_axis_title": "Air pressure",
            "y_axis_format": "atm",    
        }
    }

    st.markdown(f"# Sensor {sensor_name}")
    checkbox = st.checkbox("Expand", key=sensor_name)
    col1, col2 = st.beta_columns(2)
    with col1:
        render_altair_chart(selected_date_range, chart_settings['temperature'])
        render_altair_chart(selected_date_range, chart_settings['light_intensity'])
    with col2:
        render_altair_chart(selected_date_range, chart_settings['humidity'])
        render_altair_chart(selected_date_range, chart_settings['air_pressure'])

    location = "unknown"
    sensors = {
        "Location": "unkown",
        "Temperature": "unknown",
        "Humidity": "unknown",
        "Light intesity": "unknown",
    }
    if checkbox:
        for k, v in sensors.items():
            f"{k}={v}"
    else:
        pass


def render_altair_chart(selected_date_range, chart_settings):
    df = selected_date_range.reset_index()

    # chart_settings
    y_axis = alt.Axis(title=chart_settings['y_axis_title'])
    x_axis = alt.Axis(title=chart_settings['x_axis_title'])

    c = (
        alt.Chart(df)
        .mark_line()
        .encode(
            # x=chart_settings["x_axis_col_name"],
            # y=chart_settings["y_axis_col_name"],
            y=alt.Y(chart_settings['y_axis_col_name'], axis=y_axis),
            x=alt.X(chart_settings['x_axis_col_name'], axis=x_axis)
            # y=alt.Y(chart_settings['y_axis_col_name'], axis=y_axis),
        )
        .properties(title=chart_settings["title"])
        .configure_axis(
            labelFontSize=16,
            titleFontSize=16
        )
        .configure_title(fontSize=20)
        .interactive()
    )

    st.altair_chart(c, use_container_width=True)


_max_width_()

# data
midpoint = get_midpoint()
sensor_locations = get_sensor_locations()
sensor_dict = get_multiple_sensor_data(get_singular_sensor_data)
min_date, max_date = get_min_max_date(sensor_dict)


# sidebar
(
    level_selection,
    sensor_selection,
    sensor_type_bools,
    start_date,
    end_date,
) = render_sidebar_sensor_filters(sensor_locations, min_date, max_date)

if level_selection == 'all':
    pass
    selected_sensors = sensor_locations
else:
    selected_sensors =sensor_locations[sensor_locations.level == int(level_selection)]

# main chart
st.title("Sensor dashboard")
render_pydeck_chart(midpoint, selected_sensors)


# sensor list
render_sensor_list(sensor_dict, start_date, end_date)
