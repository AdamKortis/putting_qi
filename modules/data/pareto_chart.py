import pandas as pd
from matplotlib import pyplot

class ParetoChart():
    def __init__(self, df: pd.DataFrame):
        self.df = df

        self.failures = ['High'
                         , 'High-Right'
                         , 'Right'
                         , 'Low-Right'
                         , 'Low'
                         , 'Low-Left'
                         , 'Left'
                         , 'High-Left'
                         , 'Chain Out'
                         , 'Foot Fault']
        self.total_failures = []
        self.total_misses = 0
        self.cumulative_percent = []

    def create_failures(self):
        ...

    def create_total_misses(self):
        ...

    def create_cumulative_percent(self):
        ...
