import streamlit as st


def render_sensor_dropdown(sensor_locations):
    selection_options = ["all", None] + sensor_locations
    selection = st.sidebar.selectbox("Choose point ID", selection_options)
    return selection


def render_level_dropdown(unique_sensor_levels):
    possible_levels = ["all", None] + unique_sensor_levels
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

    sensor_types = [
        s_type for s_type, s_bool in sensor_type_bools.items() if s_bool == True
    ]
    return sensor_types


def render(unique_sensor_levels, sensor_list, min_date, max_date):
    filters = {}

    st.sidebar.header("Filter sensors")
    filters["level_selection"] = render_level_dropdown(unique_sensor_levels)
    filters["sensor_selection"] = render_sensor_dropdown(sensor_list)

    st.sidebar.header("Filter dates")
    filters["start_date"] = render_start_date_selection(min_date, max_date)
    filters["end_date"] = render_end_date_selection(min_date, max_date)

    st.sidebar.header("Filter sensor types")
    filters["sensor_types"] = render_sensor_type_checkboxes()

    return filters
