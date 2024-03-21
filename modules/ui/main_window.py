import tkinter as tk
from tkinter.ttk import Frame, Label, Entry, Button

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        x = int(self.winfo_screenwidth() / 2 - 640)
        y = int(self.winfo_screenheight() / 2 - 360)

        self.geometry(f'1280x720+{x}+{y}')
        self.title('QI Putting App')

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
                            , 'Foot Fault']
        
        # date frame variables
        self.date_frame = Frame(self)
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
                                , 'Total'
                                , 'Percent Made']
        
        # putt frames
        self.putt_frames = []
        self.putt_variables = []

        # row total/percent frames
        self.row_total_frames = []
        self.row_percent_frames = []
        self.row_total_variables = []
        self.row_percent_variables = []
        
        self.execute()

    def execute(self):
        self.create_date_label()
        self.create_top_labels()
        self.create_distance_labels()   
        self.create_putt_frames()   

    def create_date_label(self):
        Label(self.date_frame, text='Date').pack()
        Entry(self.date_frame, textvariable=self.entry_date).pack()
        self.date_frame.grid(row=0, column=0, columnspan=14)

    def create_top_labels(self):
        for x, name in enumerate(self.top_labels):
            frame = Frame(self)
            Label(frame, text=name).pack()
            self.top_label_frames.append(frame)
            frame.grid(row=1, column=x)

    def create_distance_labels(self):
        for x, name in enumerate(self.distance_labels):
            frame = Frame(self)
            Label(frame, text=name).pack()
            self.distance_label_frames.append(frame)
            frame.grid(row=x+2, column=0)

    def create_putt_frames(self):
        for x in range(5):
            temp_frames = []
            temp_variables = []
            for y in range(11):
                frame = Frame(self)
                var_count = tk.IntVar(frame, value=0)
                Label(frame, textvariable=var_count).grid(row=0, column=0, columnspan=2)
                Button(frame, text='+', width=5).grid(row=1, column=0)
                Button(frame, text='-', width=5).grid(row=1, column=1)
                frame.grid(row=x+2, column=y+1)
                temp_frames.append(frame)
                temp_variables.append(var_count)
            self.putt_frames.append(temp_frames)
            self.putt_variables.append(temp_variables)

    def create_total_percent_frames(self):
        pass
                