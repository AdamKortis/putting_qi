from os.path import isfile
from os import getcwd
import pandas as pd
from modules.data.pareto_chart import ParetoChart
from modules.data.control_chart import ControlChart
from datetime import datetime

DATA_FILE = f'{getcwd()}/files/csv/putt_data.csv'

def submit_data(date: datetime, putt_data: list):
    if file_check():
        df = pd.read_csv(DATA_FILE, header=0, sep='|')
    else:
        header='Date|Distance|Made|High|High-Right|Right|Low-Right|Low|Low-Left|Left|High-Left|Chain Out|Foot Fault\n'
        f = open(DATA_FILE, 'w')
        f.write(header)
        f.close()
        df = pd.read_csv(DATA_FILE, header=0, sep='|')
    for x, row_data in enumerate(putt_data):
        if x == 0:
            distance = 2
        elif x == 1:
            distance = 4
        elif x == 2:
            distance = 6
        elif x == 3:
            distance = 8
        elif x == 4:
            distance = 10
        else:
            distance = 0
        putt_data = [date, distance] + [x.get() for x in row_data]
        df.loc[len(df)] = putt_data
    df.to_csv(DATA_FILE, header=True, index=False, sep='|')

def file_check():
    return isfile(DATA_FILE)

def load_file():
    return pd.read_csv(DATA_FILE, header=0, sep='|')

def create_pareto_chart(distance: str):
    df = load_file()
    df.sort_values(by='Date', inplace=True)
    if distance is not None and distance != 'all':
        pareto_chart = ParetoChart(df, distance)
    else:
        pareto_chart = ParetoChart(df)
    return pareto_chart.create_pareto_chart()

def create_control_chart(distance: str):
    df = load_file()
    df.sort_values(by='Date', inplace=True)
    if distance is not None and distance != 'all':
        control_chart = ControlChart(df, distance)
    else:
        control_chart = ControlChart(df)
    return control_chart.create_control_chart()