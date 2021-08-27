import pandas as pd
from typing import Dict, Tuple, List

def get_midpoint():
    return {"lat": 52.3671182, "lon": 4.9038155}
    # return {"lat": 49.196, "lon": -123.0}


def get_sensor_locations():
    sensor_locations = pd.read_csv("data/clean/sensor_locations.csv")
    sensor_locations = sensor_locations.round(8)
    unique_sensor_levels = list(sensor_locations["level"].unique())
    return sensor_locations, unique_sensor_levels


def get_measurements(sensor_names:List) -> pd.DataFrame:
    
    measurements = []
    for sensor_name in sensor_names:
        measurements_sensor = get_singular_sensor_data(sensor_name)
        measurements_sensor['sensor'] = sensor_name
        measurements.append(measurements_sensor)
    
    measurements = pd.concat(measurements)
    min_date, max_date = get_min_max_date(measurements)
    measurements = measurements.set_index('date').sort_index()
    return measurements, min_date, max_date

def get_min_max_date(measurements):
    min_date = measurements.date.min()
    # if len(min_date) > 1:
        # min_date = min_date.min()
    max_date = measurements.date.max()
    # if len(max_date) > 1:
        # max_date = max_date.max()
    return min_date, max_date

def get_singular_sensor_data(sensor_name):
    sensor_data = pd.read_csv(
        f"data/clean/vorigemaand_clean_sensor_{sensor_name}.csv", index_col=0
    )
    sensor_data.date = pd.to_datetime(sensor_data.date, format="%Y%m%d %H")
    
    return sensor_data



def get_chart_settings():
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
        },
    }
    return chart_settings

def filter_data(sensor_locations:pd.DataFrame, measurements:pd.DataFrame, filters:Dict) -> tuple([pd.DataFrame, pd.DataFrame]):
    if filters['level_selection'] == "all":
        filtered_sensor_locations = sensor_locations
    elif filters['level_selection'] == None:
        filtered_sensor_locations = pd.DataFrame()
    else:
        filtered_sensor_locations = sensor_locations[sensor_locations.level == int(filters['level_selection'])]

    filtered_measurements = measurements
    filtered_measurements = filtered_measurements.loc[filters['start_date']:filters['end_date']]

    filtered_columns = ['sensor'] + filters['sensor_types']
    filtered_measurements = filtered_measurements.loc[:, filtered_columns]

    return filtered_sensor_locations, filtered_measurements
    