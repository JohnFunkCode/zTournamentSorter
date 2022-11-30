import tkinter as tk
from tkinter import ttk


class SpashScreen(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}

        # data table label
        self.opening_label0 = ttk.Label(self, text='zUltimate Tournament App',font="Helventica 22 bold")
        self.opening_label0.grid(column=0, row=0,**options)
        self.image =  tk.PhotoImage(file='./GUI/splashscreen/zTournament_Colorado_1721x972.png')
        self.image_lable=ttk.Label(self, image=self.image).grid(column=0, row=1,rowspan=2,**options)

    def show_view(self):
        self.grid()

    def hide_view(self):
        self.grid_forget()


