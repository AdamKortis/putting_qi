import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

class ControlChart():
    def __init__(self, df: pd.DataFrame):
        self.df = df

        self.run = True if len(self.df) >= 12 else False
        self.control = True if len(self.df) >= 20 else False

        self.x_values = []
        self.y_values = []
        self.x_points = []
        self.centerline = []
        self.ucl = []
        self.lcl = []
        self.colors = []
        self.markers = []

        self.execute()

    def execute(self):
        self.create_data_points()
        self.create_x_y_values()
        self.create_x_points()
        self.create_centerline()
        self.create_upper_control_limit()
        self.create_lower_control_limit()
        self.flag_above_centerline()
        self.flag_below_centerline()
        self.flag_shift_up()
        self.flag_shift_down()

    def create_data_points(self):
        self.df['Total Putts'] = self.df[['Made'
                                    , 'High'
                                    , 'High-Right'
                                    , 'Right'
                                    , 'Low-Right'
                                    , 'Low'
                                    , 'Low-Left'
                                    , 'Left'
                                    , 'High-Left'
                                    , 'Chain Out'
                                    , 'Foot Fault']].sum(axis=1)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df = self.df.groupby('Date')[['Made', 'Total Putts']].sum()
        self.df.reset_index(inplace=True)
        self.df['data_point'] = (self.df['Made'] / self.df['Total Putts']) * 100

    def create_x_y_values(self):
        self.x_values = list(self.df['Date'].values)
        self.y_values = list(self.df['data_point'].values)
    
    def create_x_points(self):
        self.x_points = [x for x in range(len(self.x_values))]

    def create_centerline(self):
        temp_df = self.df.head(20).copy()
        self.df['centerline'] = (temp_df['Made'].sum() / temp_df['Total Putts'].sum()) * 100
        self.centerline = list(self.df['centerline'].values)

    def create_upper_control_limit(self):
        self.df['ucl'] = self.df['centerline'] + (3 * np.sqrt((self.df['centerline'] * (100 - self.df['centerline']))/20))
        self.ucl = list(self.df['ucl'].values)

    def create_lower_control_limit(self):
        self.df['lcl'] = self.df['centerline'] - (3 * np.sqrt((self.df['centerline'] * (100 - self.df['centerline']))/20))
        self.df['lcl'] = list(self.df['lcl'].values)

    def flag_above_centerline(self):
        self.df['above_centerline'] = 0
        self.df.loc[self.df['data_point'] > self.df['centerline'], 'above_centerline'] = 1

    def flag_below_centerline(self):
        self.df['below_centerline'] = 0
        self.df.loc[self.df['data_point'] < self.df['centerline'], 'below_centerline'] = 1

    def flag_shift_up(self):
        self.df['shift_up'] = 0
        shift_up = []
        for index, row in self.df.iterrows():
            if row['above_centerline'] == 1:
                shift_up.append(index)
            else:
                if len(shift_up) >= 8:
                    for x in shift_up:
                        self.df.loc[x, 'shift_up'] = 1
                shift_up = []
        if len(shift_up) >= 8:
            for x in shift_up:
                self.df.loc[x, 'shift_up'] = 1

    def flag_shift_down(self):
        self.df['shift_down'] = 0
        shift_down = []
        for index, row in self.df.iterrows():
            if row['below_centerline'] == 1:
                shift_down.append(index)
            else:
                if len(shift_down) >= 8:
                    for x in shift_down:
                        self.df.loc[x, 'shift_down'] = 1
                shift_down = []
        if len(shift_down) >= 8:
            for x in shift_down:
                self.df.loc[x, 'shift_down'] = 1

    def create_marker_formats(self):
        for index, row in self.df.iterrows():
            if row['shift_up'] == 1:
                self.colors.append('green')
                self.markers.append('^')
            elif row['shift_down'] == 1:
                self.colors.append('red')
                self.markers.append('v')
            else:
                self.colors.append('blue')
                self.markers.append('o')

    def create_control_chart(self):
        fig = plt.figure(figsize=(10,5))
        if not self.run and not self.control:
            for x, y in zip(self.x_points, self.y_values):
                plt.scatter(x, y, color='blue', marker='o')
        elif self.run and not self.control:
            plt.plot(self.x_points, self.y_values, color='blue', marker='o')
        elif self.run and self.control:
            plt.plot(self.x_points, self.y_values, color='blue')
            plt.plot(self.x_points, self.centerline, color='red')
            plt.plot(self.x_points, self.ucl, color='gray', style='dashed')
            plt.plot(self.x_points, self.lcl, color='gray', style='dashed')
            for x, y, c, m in zip(self.x_points, self.y_values, self.colors, self.markers):
                plt.scatter(x, y, color=c, marker=m)
        plt.xticks(self.x_points, labels=self.x_values)
        return fig
        

        