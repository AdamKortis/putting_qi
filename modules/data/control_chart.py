import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
from os import getcwd

class ControlChart():
    def __init__(self, df: pd.DataFrame, distance: str = None, start_date: str = None, stop_date: str = None):
        self.df = df 
        self.distance = distance
        self.start_date = start_date
        self.stop_date = stop_date

        self.run = True if len(list(self.df['Date'].drop_duplicates().values)) >= 8 else False
        self.control = True if len(list(self.df['Date'].drop_duplicates().values)) >= 20 else False

        self.chart_range = [None, None]

        self.x_values = []
        self.y_values = []
        self.x_points = []
        self.median = []
        self.centerline = []
        self.ucl = []
        self.lcl = []
        self.colors = []
        self.markers = []

        self.centerline_df = pd.read_csv(f'{getcwd()}/files/csv/centerlines.csv'
                                           , header=0
                                           , sep='|')

        self.execute()

    def execute(self):
        if self.distance is not None and self.distance != '':
            self.df = self.df.loc[self.df['Distance'] == int(self.distance)]
        self.create_data_points()
        self.create_x_y_values()
        self.create_x_points()
        if self.run:
            self.create_median_centerline()
        if self.control:
            self.create_centerline()
            self.create_upper_control_limit()
            self.create_lower_control_limit()
            self.flag_above_centerline()
            self.flag_below_centerline()
            self.flag_shift_up()
            self.flag_shift_down()
            self.create_marker_formats()
        date_list = list(self.df['Date'].drop_duplicates().values)
        date_list = [str(x)[:10] for x in date_list]
        if self.start_date is not None and self.start_date != '':
            self.chart_range[0] = date_list.index(self.start_date)
        else:
            self.chart_range[0] = 0
        if self.stop_date is not None and self.start_date != '':
            self.chart_range[1] = date_list.index(self.stop_date) + 1
        else:
            self.chart_range[1] = self.df.shape[0]
        self.subset_lists()

    def subset_lists(self):
        self.x_values = self.x_values[self.chart_range[0]: self.chart_range[1]]
        self.y_values = self.y_values[self.chart_range[0]: self.chart_range[1]]
        self.x_points = self.x_points[self.chart_range[0]: self.chart_range[1]]
        self.median = self.median[self.chart_range[0]: self.chart_range[1]]
        self.centerline = self.centerline[self.chart_range[0]: self.chart_range[1]]
        self.ucl = self.ucl[self.chart_range[0]: self.chart_range[1]]
        self.lcl = self.lcl[self.chart_range[0]: self.chart_range[1]]
        self.colors = self.colors[self.chart_range[0]: self.chart_range[1]]
        self.markers = self.markers[self.chart_range[0]: self.chart_range[1]]

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
        try:
            self.df['data_point'] = (self.df['Made'] / self.df['Total Putts']) * 100
        except ZeroDivisionError:
            self.df['data_point'] = 0

    def create_x_y_values(self):
        self.x_values = [pd.to_datetime(x).strftime('%m/%d/%y') for x in self.df['Date'].values]
        self.y_values = list(self.df['data_point'].values)
    
    def create_x_points(self):
        self.x_points = [x for x in range(len(self.x_values))]

    def create_median_centerline(self):
        self.df['median'] = self.df['data_point'].median()
        self.median = list(self.df['median'].values)

    def create_centerline(self):
        temp_df = self.df.head(20).copy()
        self.df['centerline'] = (temp_df['Made'].sum() / temp_df['Total Putts'].sum()) * 100
        self.centerline = list(self.df['centerline'].values)
        self.add_other_centerlines()

    def add_other_centerlines(self):
        if self.distance is not None and self.distance != '':
            self.centerline_df = self.centerline_df.loc[self.centerline_df['distance'] == self.distance]
        else:
            self.centerline_df = self.centerline_df.loc[self.centerline_df['distance'] == 'all']
        if self.centerline_df.shape[0] == 0:
            return
        for col in ('start_date', 'end_date', 'calc_start_date', 'calc_end_date'):
            self.centerline_df[col] = pd.to_datetime(self.centerline_df[col])
        for index, row in self.centerline_df.iterrows():
            calc_start_bool = self.df['Date'] >= row['calc_start_date']
            calc_end_bool = self.df['Date'] <= row['calc_end_date']
            temp_df = self.df.loc[(calc_start_bool & calc_end_bool)].copy()
            centerline = (temp_df['Made'].sum() / temp_df['Total Putts'].sum()) * 100
            start_bool = self.df['Date'] >= row['start_date']
            end_bool = self.df['Date'] <= row['end_date']
            self.df.loc[(start_bool & end_bool), 'centerline'] = centerline
            self.centerline = list(self.df['centerline'].values)

    def create_upper_control_limit(self):
        self.df['ucl'] = self.df['centerline'] + (3 * np.sqrt((self.df['centerline'] * (100 - self.df['centerline']))/20))
        self.df.loc[self.df['ucl'] > 100, 'ucl'] = 100
        self.ucl = list(self.df['ucl'].values)

    def create_lower_control_limit(self):
        self.df['lcl'] = self.df['centerline'] - (3 * np.sqrt((self.df['centerline'] * (100 - self.df['centerline']))/20))
        self.df.loc[self.df['lcl'] < 0, 'lcl'] = 0
        self.lcl = list(self.df['lcl'].values)

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
        fig = plt.figure(figsize=(10,6))
        if not self.run and not self.control:
            for x, y in zip(self.x_points, self.y_values):
                plt.scatter(x, y, color='blue', marker='o')
        elif self.run and not self.control:
            plt.plot(self.x_points, self.y_values, color='blue', marker='o')
            plt.plot(self.x_points, self.median, color='red')
            plt.annotate(str(round(self.median[0], 2))+'%', (self.x_points[0], self.median[0]))
        elif self.run and self.control:
            plt.plot(self.x_points, self.y_values, color='blue')
            plt.plot(self.x_points, self.centerline, color='red')
            plt.plot(self.x_points, self.ucl, color='gray', linestyle='dashed')
            plt.plot(self.x_points, self.lcl, color='gray', linestyle='dashed')
            for x, y, c, m in zip(self.x_points, self.y_values, self.colors, self.markers):
                plt.scatter(x, y, color=c, marker=m)
            plt.annotate(str(round(self.centerline[0], 2))+'%', (self.x_points[0], self.centerline[0]))
            plt.annotate(str(round(self.centerline[-1], 2))+'%', (self.x_points[-1], self.centerline[-1]))
        plt.xticks(self.x_points, labels=self.x_values, rotation=90, fontsize=8)
        return fig
        

        