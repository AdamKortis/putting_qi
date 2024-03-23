import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Frame, Label, Entry, Button, Notebook
from datetime import datetime
from modules.handlers.data_handlers import *
import pandas as pd
from modules.data.pareto_chart import ParetoChart

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        x = int(self.winfo_screenwidth() / 2 - 640)
        y = int(self.winfo_screenheight() / 2 - 360)

        self.geometry(f'1280x720+{x}+{y}')
        self.title('QI Putting App')
        
        # Notebooks
        self.main_tabs = Notebook(self)

        # main tab frames
        self.input_tab = Frame(self.main_tabs)
        self.pareto_tab = Frame(self.main_tabs)
        self.control_tab = Frame(self.main_tabs)
        
        # date frame variables
        self.date_frame = Frame(self.input_tab)
        self.entry_date = tk.StringVar()
        
        # top label frame variables
        self.top_label_frames = []
        self.top_labels = ['Distance from Basket'
                            , 'Made'
                            , 'Missed High'
                            , 'Missed High/Right'
                            , 'Missed Right'
                            , 'Missed Low/Right'
                            , 'Missed Low'
                            , 'Missed Low/Left'
                            , 'Missed Left'
                            , 'Missed High/Left'
                            , 'Chain Out'
                            , 'Foot Fault'
                            , 'Total'
                            , 'Percent Made']
        
        # distance labels
        self.distance_label_frames = []
        self.distance_labels = ['2 Meters'
                                , '4 Meters'
                                , '6 Meters'
                                , '8 Meters'
                                , '10 Meters'
                                , 'Total']
        
        # putt frames
        self.putt_frames = []
        self.putt_variables = []

        # row total/percent frames
        self.row_total_frames = []
        self.row_percent_frames = []
        self.row_total_variables = []
        self.row_percent_variables = []
        
        # column total/percent frames
        self.col_total_frames = []
        self.col_total_variables = []

        # aggregate total frames
        self.aggregate_total_frame = Frame(self.input_tab)
        self.aggregate_percent_frame = Frame(self.input_tab)
        self.aggregate_total_variable = tk.IntVar(self.aggregate_total_frame, value=0)
        self.aggregate_percent_variable = tk.StringVar(self.aggregate_total_frame, value='0%')

        # create submit frame
        self.submit_frame = Frame(self.input_tab)
        
        self.execute()

    def execute(self):
        self.create_date_label()
        self.create_top_labels()
        self.create_distance_labels()   
        self.create_putt_frames()   
        self.create_row_total_frames()
        self.create_col_total_frames()
        self.create_aggregate_frames()
        self.create_submit_frame()
        self.check_for_data()
        self.add_tabs()        

    def add_tabs(self):
        self.input_tab.pack()
        self.pareto_tab.pack()
        self.control_tab.pack()
        self.main_tabs.add(self.input_tab, text='Putt Data')
        self.main_tabs.add(self.pareto_tab, text='Pareto Chart')
        self.main_tabs.add(self.control_tab, text='Control Chart')
        self.main_tabs.pack()

    def create_date_label(self):
        Label(self.date_frame, text='Date:').pack()
        Label(self.date_frame, text='(MM/DD/YYYY)').pack()
        Entry(self.date_frame, textvariable=self.entry_date).pack()
        self.date_frame.grid(row=0, column=0, columnspan=14)

    def create_top_labels(self):
        for x, name in enumerate(self.top_labels):
            frame = Frame(self.input_tab)
            Label(frame, text=name).pack()
            self.top_label_frames.append(frame)
            frame.grid(row=1, column=x)

    def create_distance_labels(self):
        for x, name in enumerate(self.distance_labels):
            frame = Frame(self.input_tab)
            Label(frame, text=name).pack()
            self.distance_label_frames.append(frame)
            frame.grid(row=x+2, column=0)

    def create_putt_frames(self):
        for x in range(5):
            temp_frames = []
            temp_variables = []
            for y in range(11):
                frame = Frame(self.input_tab)
                var_count = tk.IntVar(frame, value=0)
                Label(frame, text=str(var_count.get()), textvariable=var_count).grid(row=0, column=0, columnspan=2)
                Button(frame, text='+', width=5, command=lambda row=x, column=y: self.increase(row, column)).grid(row=1, column=0)
                Button(frame, text='-', width=5, command=lambda row=x, column=y: self.decrease(row, column)).grid(row=1, column=1)
                frame.grid(row=x+2, column=y+1)
                temp_frames.append(frame)
                temp_variables.append(var_count)
            self.putt_frames.append(temp_frames)
            self.putt_variables.append(temp_variables)

    def create_row_total_frames(self):
        for x in range(5):
            total_frame = Frame(self.input_tab)
            percent_frame = Frame(self.input_tab)
            var_total = tk.IntVar(total_frame, value=0)
            var_percent = tk.StringVar(percent_frame, value='0%')
            Label(total_frame, text=var_total.get(), textvariable=var_total).pack()     
            Label(percent_frame, textvariable=var_percent).pack()
            total_frame.grid(row=x+2, column=13)  
            percent_frame.grid(row=x+2, column=14)
            self.row_total_frames.append(total_frame)
            self.row_percent_frames.append(percent_frame)
            self.row_total_variables.append(var_total)
            self.row_percent_variables.append(var_percent)         

    def create_col_total_frames(self):
        for y in range(11):
            total_frame = Frame(self.input_tab)
            var_total = tk.IntVar(total_frame, value=0)
            Label(total_frame, text=var_total.get(), textvariable=var_total).pack()
            total_frame.grid(row=7, column=y+1)
            self.col_total_frames.append(total_frame)
            self.col_total_variables.append(var_total)
            
    def create_aggregate_frames(self):
        Label(self.aggregate_total_frame, textvariable=self.aggregate_total_variable).pack()
        Label(self.aggregate_percent_frame, textvariable=self.aggregate_percent_variable).pack()
        self.aggregate_total_frame.grid(row=7, column=13)
        self.aggregate_percent_frame.grid(row=7, column=14)

    def create_submit_frame(self):
        Button(self.submit_frame, text='Submit Data', command=self.submit_data).pack()
        self.submit_frame.grid(row=8, column=0, columnspan=13)

    def increase(self, row, column):
        self.putt_variables[row][column].set(self.putt_variables[row][column].get() + 1)
        self.increase_row_total(row)
        self.increase_col_total(column)
        self.increase_aggregate_total()
        self.update_row_percent(row)
        self.update_aggregate_percent()
        self.update()

    def decrease(self, row, column):
        if self.putt_variables[row][column].get() <= 0:
            self.putt_variables[row][column].set(0)
        else:
            self.putt_variables[row][column].set(self.putt_variables[row][column].get() - 1)
            self.decrease_row_total(row)
            self.decrease_col_total(column)
            self.decrease_aggregate_total()
            self.update_row_percent(row)
            self.update_aggregate_percent()
        self.update()

    def increase_row_total(self, row):
        self.row_total_variables[row].set(self.row_total_variables[row].get() + 1)

    def decrease_row_total(self, row):
        if self.row_total_variables[row].get() <= 0:
            self.row_total_variables[row].set(0)
        else:
            self.row_total_variables[row].set(self.row_total_variables[row].get() - 1)

    def increase_col_total(self, col):
        self.col_total_variables[col].set(self.col_total_variables[col].get() + 1)

    def decrease_col_total(self, col):
        if self.col_total_variables[col].get() <= 0:
            self.col_total_variables[col].set(0)
        else:
            self.col_total_variables[col].set(self.col_total_variables[col].get() - 1)

    def increase_aggregate_total(self):
        self.aggregate_total_variable.set(self.aggregate_total_variable.get() + 1)

    def decrease_aggregate_total(self):
        if self.aggregate_total_variable.get() <= 0:
            self.aggregate_total_variable.set(0)
        else:
            self.aggregate_total_variable.set(self.aggregate_total_variable.get() - 1)

    def update_row_percent(self, row):
        percent = (self.putt_variables[row][0].get() / self.row_total_variables[row].get()) * 100
        self.row_percent_variables[row].set(f'{round(percent, 2)}%')

    def update_aggregate_percent(self):
        percent = (self.col_total_variables[0].get() / self.aggregate_total_variable.get()) * 100
        self.aggregate_percent_variable.set(f'{round(percent, 2)}%')

    def submit_data(self):
        entry_date = self.check_date()
        if entry_date == datetime(9999, 1, 1):
            messagebox.showerror('Incorrect Date Format', 'Date should be of the following format: MM/DD/YYYY.')
            return None
        if self.aggregate_total_variable.get() == 0:
            messagebox.showerror('No Data', 'You have not entered any data.')
            return None
        submit_data(self.putt_variables)
        self.clear_fields()

    def check_date(self):
        try:
            putt_date = datetime.strptime(self.entry_date.get(), '%m/%d/%Y')
        except TypeError:
            putt_date = datetime.strptime('01/01/9999', '%m/%d/%Y')
        except ValueError:
            putt_date = datetime.strptime('01/01/9999', '%m/%d/%Y')
        return putt_date
    
    def clear_fields(self):
        self.entry_date.set('')
        for x in self.putt_variables:
            for y in x:
                y.set(0)
        for x in self.row_total_variables:
            x.set(0)
        for x in self.row_percent_variables:
            x.set('0%')
        for x in self.col_total_variables:
            x.set(0)
        self.aggregate_total_variable.set(0)
        self.aggregate_percent_variable.set('0%')

    def check_for_data(self):
        if not file_check():
            Label(self.pareto_tab, text='No data to display.').pack()
            Label(self.control_tab, text='No data to display.').pack()
        else:
            create_pareto_chart()