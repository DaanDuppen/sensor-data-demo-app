

import math
import pandas as pd
import matplotlib.pyplot as plt

def generate_x(hour_iterator):
    x = [i for i in hour_iterator]
    return x

def show_scatter_plot(x, y):
    plt.plot(x, y)
    plt.scatter(x, y,  alpha=0.5)
    plt.show()

def generate_y(hour_iterator):
    base_temp = 21
    temp_amplitude = 5

    b = 0.024

    period = 2 * math.pi / b
    print(period)

    y = []
    # for hour in hour_iterator:
    for minute in hour_iterator:
        temp = temp_amplitude * math.sin(minute/ period ) + base_temp
        y.append(temp)
    return y

# def generate_y_new(hour_iterator):
#     for hour in hour_iterator:


if __name__ == '__main__':
    # hour_iterator = range(0, 24)
    # y = generate_y(hour_iterator)
    # x = generate_x(hour_iterator)
    # show_scatter_plot(x, y)

    df = pd.read_csv('vorigemaand.csv')
    df.columns = df.columns.str.strip()
    cols_to_keep = ['YYYYMMDD', 'HH', 'T', '# STN']
    df = df.loc[:, cols_to_keep]
    df = df.rename(columns={'YYYYMMDD':'date', '# STN':'station_number'})
    df = df.loc[14914:15657]
    df = df.loc[df['station_number'] == 279]
    df = df.drop(columns=['station_number']).reset_index()
    df['T'] = pd.to_numeric(df['T'])
    df['T'] = df['T'] / 10
    df['HH'] = df['HH'].apply(str).str.zfill(2)
    df.loc[df['HH'] == '24', 'HH'] = '00'
    df['date'] = df['date'].apply(str)
    df['date'] = df['date'] + ' ' + df['HH']
    df = df.drop(columns=['HH'])
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d %H')
    df['sensor'] = 'sensor 1-1'
    df.to_csv('vorigemaand_clean.csv')

    df


    # df = pd.read_csv('vorigemaand_clean.csv', index_col=0)
    # df.plot(x='date', y='T')
    # plt.show()
    # print('daan')