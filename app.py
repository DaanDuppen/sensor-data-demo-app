import streamlit as st
import pandas as pd
from src.components import map_component
from src.components import sensor_list_component
from src.components import filter_component
from src.helpers.data_helpers import filter_data, get_midpoint, get_measurements, get_sensor_locations, get_chart_settings
from src.helpers.html_inject import _max_width_


# streamlit run app.py
# https://share.streamlit.io/daanduppen/sensor-data-demo-app/main/app.py

# Done
# clean up code
# expanders for sensor cards
# host

# add
# make filters an object
# add overview plots to show gained heat
# add prediction graphs
# add overview of building energy consumption
# make building level and point id filters work
# color each selected dot
# 3D walls? areas?
# levels

# CHECK COLUMNS WITH PABLO PACKAGE?
# Do I get back all points when I clear filters? 

def render_page(filters):  
    _max_width_()

    # load all required data
    midpoint = get_midpoint()
    sensor_locations, unique_sensor_levels = get_sensor_locations()
    sensor_list = ['1-1', '1-2']
    measurements, min_date, max_date = get_measurements(sensor_list)
    chart_settings = get_chart_settings()
    filtered_sensor_locations = pd.DataFrame()
    
    # render components
    st.title("Sensor dashboard")

    st.header("Sensor location map")
    map_component.render(midpoint, sensor_locations, filtered_sensor_locations)
    filters = filter_component.render(unique_sensor_levels, sensor_list, min_date, max_date)
    filtered_sensor_locations, filtered_measurements = filter_data(sensor_locations, measurements, filters)
    st.header("Sensor details")
    sensor_list_component.render(chart_settings, filtered_sensor_locations, filtered_measurements)

if __name__ == "__main__":
    filters = {
    'level_selection': None,
    'sensor_selection': None,
    'start_date': None,
    'end_date': None,
    'sensor_type_bools': None
    }

    render_page(filters)