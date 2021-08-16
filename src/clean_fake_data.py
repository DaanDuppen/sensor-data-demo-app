import pandas as pd
import matplotlib.pyplot as plt


def show_scatter_plot(x, y):
    plt.plot(x, y)
    plt.scatter(x, y, alpha=0.5)
    plt.show()


def strip_column_names(df):
    df.columns = df.columns.str.strip()
    return df


def rename_columns(df, column_name_mapper):
    df = df.rename(columns=column_name_mapper)
    return df


def filter_columns(df, columns_to_keep):
    df = df.loc[:, columns_to_keep]
    return df


def select_rows_by_station(df, station_number):
    df = df.loc[df["station_number"] == station_number]
    df = df.drop(columns=["station_number"]).reset_index()
    return df


def fix_temperature_column(df):
    df["temperature"] = pd.to_numeric(df["temperature"])
    df["temperature"] = df["temperature"] / 10
    return df


def fix_hour_column(df):
    df["hour"] = df["hour"].apply(str).str.zfill(2)
    df.loc[df["hour"] == "24", "hour"] = "00"
    return df


def fix_date_column(df):
    df["date"] = df["date"].apply(str)
    df["date"] = df["date"] + " " + df["hour"]
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d %H")
    return df


if __name__ == "__main__":
    column_name_mapper = {
        "YYYYMMDD": "date",
        "# STN": "station_number",
        "HH": "hour",
        "T": "temperature",
    }
    columns_to_keep = ["date", "hour", "temperature", "station_number"]

    # df = df.set_index('date')

    # df["sensor"] = "sensor 1-1"

    # df["start_day"] = False
    # mask = df.date.dt.hour == 0
    # df.loc[mask, "start_day"] = True


    sensor_name_to_station_number_map_dict = {"1-1": 279, '1-2': 391}
    raw_df = pd.read_csv("data/raw/vorigemaand.csv")
    raw_df

    for sensor_name, station_number in sensor_name_to_station_number_map_dict.items():
        sensor_df = (
            raw_df
            .pipe(strip_column_names)
            .pipe(rename_columns, column_name_mapper)
            .pipe(filter_columns, columns_to_keep)
            .pipe(select_rows_by_station, station_number)
            .pipe(fix_temperature_column)
            .pipe(fix_hour_column)
            .pipe(fix_date_column)
        )

        sensor_df['humidity'] = sensor_df['temperature']
        sensor_df['light_intensity'] = sensor_df['temperature']
        sensor_df['air_pressure'] = sensor_df['temperature']

        sensor_df = sensor_df.drop(columns=["index"])
        sensor_df = sensor_df.drop(columns=["hour"])

        sensor_df.to_csv(f"data/vorigemaand_clean_sensor_{sensor_name}.csv")

    sensor_df

    # df = pd.read_csv('vorigemaand_clean.csv', index_col=0)
    # df.plot(x='date', y='temperature')
    # plt.show()
    # print('daan')
