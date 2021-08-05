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
    df = pd.read_csv("data/raw/vorigemaand.csv")

    column_name_mapper = {"YYYYMMDD": "date", "# STN": "station_number", "HH":'hour', 'T':'temperature'}
    columns_to_keep = ["date", "hour", "temperature", "station_number"]
    station_number = 279
    sensor_name = '1-1'
    
    df = (
        df
        .pipe(strip_column_names)
        .pipe(rename_columns, column_name_mapper)
        .pipe(filter_columns, columns_to_keep)
        .pipe(select_rows_by_station, station_number)
        .pipe(fix_temperature_column)
        .pipe(fix_hour_column)
        .pipe(fix_date_column)
    )

    # df = df.set_index('date')
    df = df.drop(columns=["index"])
    df = df.drop(columns=["hour"])
    # df["sensor"] = "sensor 1-1"

    # df["start_day"] = False
    # mask = df.date.dt.hour == 0
    # df.loc[mask, "start_day"] = True

    df.to_csv(f"data/vorigemaand_clean_sensor_{sensor_name}.csv")

    df

    sensor_data = pd.read_csv(f"data/vorigemaand_clean_sensor_{sensor_name}.csv", index_col=0)

    # sensor_data.index = pd.to_datetime(sensor_data.index, format="%Y%m%d %H")
    sensor_data

    # df = pd.read_csv('vorigemaand_clean.csv', index_col=0)
    # df.plot(x='date', y='temperature')
    # plt.show()
    # print('daan')
