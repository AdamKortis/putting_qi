import tkinter as tk
from tkinter.ttk import Frame, Label

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        x = int(self.winfo_screenwidth() / 2 - 640)
        y = int(self.winfo_screenheight() / 2 - 360)

        self.geometry(f'1280x720+{x}+{y}')
        self.title('QI Putting App')

        self.frames = {'label_frame': Frame(self)
                       , 'two_meter_frame': Frame(self)
                       , 'four_meter_frame': Frame(self)
                       , 'six_meter_frame': Frame(self)
                       , 'eight_meter_frame': Frame(self)
                       , 'ten_meter_frame': Frame(self)
                       , 'total_frame': Frame(self)
                       , 'button_frame': Frame(self)}
        
        self.main_labels = [Label(self.frames['label_frame'], text='Distance From Basket')
                            , Label(self.frames['label_frame'], text='Made')
                            , Label(self.frames['label_frame'], text='Missed High')
                            , Label(self.frames['label_frame'], text='Missed High-Right')
                            , Label(self.frames['label_frame'], text='Missed Right')
                            , Label(self.frames['label_frame'], text='Missed Low-Right')
                            , Label(self.frames['label_frame'], text='Missed Low')
                            , Label(self.frames['label_frame'], text='Missed Low-Left')
                            , Label(self.frames['label_frame'], text='Missed Left')
                            , Label(self.frames['label_frame'], text='Missed High-Left')
                            , Label(self.frames['label_frame'], text='Chain Out')
                            , Label(self.frames['label_frame'], text='Foot Fault')
                            , Label(self.frames['label_frame'], text='Total Putts')
                            , Label(self.frames['label_frame'], text='Percent Made')]
        
        self.distance_labels = ['2 Meters', '4 Meters', '6 Meters', '8 Meters', '10 Meters', 'Total']
        
        self.grid_top_labels()
        self.grid_distance_labels()
        self.grid_frames()


    def grid_frames(self):
        for x, frame in enumerate(self.frames.values()):
            frame.grid(row=x, column=0)

    def grid_top_labels(self):
        for x, label in enumerate(self.main_labels):
            label.grid(row=0, column=x)

    def grid_distance_labels(self):
        for x, name in enumerate(self.distance_labels):
            Label(self.frames[list(self.frames.keys())[x]], text=name).grid(row=0, column=0)