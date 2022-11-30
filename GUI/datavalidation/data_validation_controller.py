import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from tkinter.messagebox import showinfo

import GUI.datavalidation.data_validation_view

class DataValidationController():
    def __init__(self, app_container: ttk.Frame):
        super().__init__()
        self.app_container = app_container
        self.data_validation_view = GUI.datavalidation.data_validation_view.DataValidationView(app_container,self)

    def hide_view(self):
        self.data_validation_view.hide_view()

    def show_view(self):
        self.data_validation_view.show_view()

    def load_tournament_file(self):
        filename = filedialog.askopenfilename(title="Select the file with the tournament data",filetypes=[("csv","*.csv")])
        self.app_container.database = pd.read_csv(filename)
        self.data_validation_view.update_table()
        self.data_validation_view.table.show()
        self.data_validation_view.show_view()

    def load_division_file(self):
        filename = filedialog.askopenfilename(title="Select the file with the division data",filetypes=[("csv","*.csv"),("excel","*.xls")])
        self.app_container.database = pd.read_csv(filename)
        self.data_validation_view.update_table()
        self.data_validation_view.table.show()
        self.data_validation_view.show_view()

    def process_data(self):
        showinfo(title='Info', message="Start processing data")

    def test_one(self):
        self.data_validation_view.highlight_age_error(11)
        self.data_validation_view.highlight_age_error(22)
        self.data_validation_view.highlight_age_error(33)

    def test_two(self):
        self.data_validation_view.goto_row_column(11,'Age')