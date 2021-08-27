import streamlit as st
import altair as alt


def render(chart_settings, selected_sensor_locations, measurements):
    for sensor_name in selected_sensor_locations.sensor.unique():
        singular_sensor_measurements = measurements[measurements.sensor == sensor_name]
        render_sensor_card(chart_settings, sensor_name, singular_sensor_measurements)


def render_sensor_card(chart_settings, sensor, singular_sensor_measurements):

    charts = {}
    for chart_type in chart_settings.keys():
        if chart_type in singular_sensor_measurements.columns:
            charts[chart_type] = generate_altair_chart(singular_sensor_measurements, chart_settings[chart_type])

    my_expander = st.expander(f"# Sensor {sensor}")
    with my_expander:

        checkbox = st.checkbox("Details", key=sensor)
        render_sensor_charts(charts)

        render_sensor_details(checkbox)

def render_sensor_details(checkbox):
    location = "unknown"
    sensors = {
            "Location": "unkown",
            "Temperature": "unknown",
            "Humidity": "unknown",
            "Light intesity": "unknown",
        }
    if checkbox:
        for k, v in sensors.items():
            st.text(f"{k}={v}")
    else:
        pass

def render_sensor_charts(charts):
    col1, col2 = st.columns(2)
    for i, chart in enumerate(charts.values()):
        with col1:
            if i % 2 == 0:
                st.altair_chart(chart, use_container_width=True)
            else:
                pass

        with col2:
            if i % 2 == 1:
                st.altair_chart(chart, use_container_width=True)
            else:
                pass
    #         else:
    #             pass
    #         render_altair_chart(singular_sensor_measurements, chart_settings["humidity"])
    # with col1:
    #     if 'light_intensity' in singular_sensor_measurements.columns:
    #         render_altair_chart(singular_sensor_measurements, chart_settings["light_intensity"])
    # with col2:
    #     if 'air_pressure' in singular_sensor_measurements.columns:
    #         render_altair_chart(singular_sensor_measurements, chart_settings["air_pressure"])


def generate_altair_chart(singular_sensor_measurements, chart_settings):
    df = singular_sensor_measurements.reset_index()

    # chart_settings
    y_axis = alt.Axis(title=chart_settings["y_axis_title"])
    x_axis = alt.Axis(title=chart_settings["x_axis_title"])

    c = (
        alt.Chart(df)
        .mark_line()
        .encode(
            # x=chart_settings["x_axis_col_name"],
            # y=chart_settings["y_axis_col_name"],
            y=alt.Y(chart_settings["y_axis_col_name"], axis=y_axis),
            x=alt.X(chart_settings["x_axis_col_name"], axis=x_axis)
            # y=alt.Y(chart_settings['y_axis_col_name'], axis=y_axis),
        )
        .properties(title=chart_settings["title"])
        .configure_axis(labelFontSize=16, titleFontSize=16)
        .configure_title(fontSize=20)
        .interactive()
    )

    return c

    
