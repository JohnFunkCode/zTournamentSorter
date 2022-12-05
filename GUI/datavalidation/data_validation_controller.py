import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from tkinter.messagebox import showinfo


from cleaninput import cleaninput
from cleaninput import rename_colums as RN
from cleaninput import input_errors

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

        errorLogFileName = filename[0:len(filename) - 4] + "-Error.txt"
        errorLogFile = open(errorLogFileName, "w")

        cleaninput.clean_unicode_from_file(filename, errorLogFile)

        # rename all the columns in the dataframe to usable names
        r = RN.RenameColumns(filename)
        r.rename_all_columns()
        renamed_df = r.get_dataframe_copy()
        input_error_list = input_errors.InputErrors()
        clean_df,error_count=cleaninput.clean_all_input_errors(renamed_df, errorLogFile, input_error_list)
        self.app_container.database =clean_df
        self.data_validation_view.update_table()

        print(f'Input Errors:{input_error_list.error_list}')
        for i in range(len(input_error_list.error_list)):
            if input_error_list.error_list[i][1]=='Age':
                self.data_validation_view.highlight_age_error(input_error_list.error_list[i][0]+1)
            if input_error_list.error_list[i][1]=='Height':
                self.data_validation_view.highlight_weight_error(input_error_list.error_list[i][0]+1)
            if input_error_list.error_list[i][1]=='Weight':
                self.data_validation_view.highlight_weight_error(input_error_list.error_list[i][0]+1)
            if input_error_list.error_list[i][1] == 'Rank':
                self.data_validation_view.highlight_rank_error(input_error_list.error_list[i][0]+1)

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