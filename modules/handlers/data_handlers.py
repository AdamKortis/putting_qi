from os.path import isfile
from os import getcwd
import pandas as pd

DATA_FILE = f'{getcwd()}/files/csv/putt_data.csv'

def submit_data(putt_data: list):
    if file_check():
        df = pd.read_csv(DATA_FILE, header=0, sep='|')
    else:
        header='d|m|hi|hir|r|lor|lo|lol|l|hil|co|ff\n'
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
        putt_data = [distance, ] + [x.get() for x in row_data]
        df.loc[len(df)] = putt_data
    df.to_csv(DATA_FILE, header=True, index=False, sep='|')

def file_check():
    return isfile(DATA_FILE)