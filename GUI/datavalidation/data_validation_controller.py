import time
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
        self.input_error_list = input_errors.InputErrors()
        self.error_cursor = 0
        self.errorLogFileName=''


    def hide_view(self):
        self.data_validation_view.hide_view()

    def show_view(self):
        self.data_validation_view.show_view()

    def load_tournament_file(self):
        filename = filedialog.askopenfilename(title="Select the file with the tournament data",filetypes=[("csv","*.csv")])

        self.errorLogFileName = filename[0:len(filename) - 4] + "-Error.txt"
        errorLogFile = open(self.errorLogFileName, "w")

        cleaninput.clean_unicode_from_file(filename, errorLogFile)

        # rename all the columns in the dataframe to usable names
        r = RN.RenameColumns(filename)
        r.rename_all_columns()
        renamed_df = r.get_dataframe_copy()
        # self.input_error_list = input_errors.InputErrors()
        clean_df,error_count=cleaninput.clean_all_input_errors(renamed_df, errorLogFile, self.input_error_list)
        self.app_container.database =clean_df
        self.data_validation_view.update_table()

        print(f'Input Errors:{self.input_error_list.error_list}')
        for i in range(len(self.input_error_list.error_list)):
            if self.input_error_list.error_list[i][1]=='Age':
                self.data_validation_view.highlight_age_error(self.input_error_list.error_list[i][0]+1)
            if self.input_error_list.error_list[i][1]=='Height':
                self.data_validation_view.highlight_weight_error(self.input_error_list.error_list[i][0]+1)
            if self.input_error_list.error_list[i][1]=='Weight':
                self.data_validation_view.highlight_weight_error(self.input_error_list.error_list[i][0]+1)
            if self.input_error_list.error_list[i][1] == 'Rank':
                self.data_validation_view.highlight_rank_error(self.input_error_list.error_list[i][0]+1)
        self.input_error_list.error_list.sort()

        errorLogFile.close()
        self.data_validation_view.table.show()
        self.data_validation_view.show_view()

        # TBD figure out how to goto the first error the first time the table is loaded - it appears the table isn't rendered yet.
        # row= self.input_error_list.error_list[self.error_cursor][0] + 1
        # column = self.input_error_list.error_list[self.error_cursor][1]
        # self.data_validation_view.goto_row_column(row,column)



    def validate_data(self):
        errorLogFile = open(self.errorLogFileName, "a")
        self.input_error_list = []
        self.input_error_list = input_errors.InputErrors()
        self.data_validation_view.reset_color()

        df=self.app_container.database
        clean_df,error_count=cleaninput.clean_all_input_errors(df, errorLogFile, self.input_error_list)
        self.app_container.database =clean_df
        self.data_validation_view.update_table()

        self.input_error_list.error_list.sort()
        print(f'{time.strftime("%X")} Input Errors:{self.input_error_list.error_list}')
        for i in range(len(self.input_error_list.error_list)):
            if self.input_error_list.error_list[i][1]=='Age':
                self.data_validation_view.highlight_age_error(self.input_error_list.error_list[i][0]+1)
                # print(f'Age:{time.strftime("%X")}')

            if self.input_error_list.error_list[i][1]=='Height':
                self.data_validation_view.highlight_height_error(self.input_error_list.error_list[i][0]+1)
                # print(f'Height:{time.strftime("%X")}')

            if self.input_error_list.error_list[i][1]=='Weight':
                self.data_validation_view.highlight_weight_error(self.input_error_list.error_list[i][0]+1)
                # print(f'Weight:{time.strftime("%X")}')

            if self.input_error_list.error_list[i][1] == 'Rank':
                self.data_validation_view.highlight_rank_error(self.input_error_list.error_list[i][0]+1)
                # print(f'Rank:{time.strftime("%X")}')

        print(time.strftime("%X"))

        errorLogFile.close()
        self.data_validation_view.table.redraw()
        self.data_validation_view.table.show()
        self.data_validation_view.show_view()
        print(time.strftime("%X"))



    def load_division_file(self):
        filename = filedialog.askopenfilename(title="Select the file with the division data",filetypes=[("csv","*.csv"),("excel","*.xls")])
        self.app_container.database = pd.read_csv(filename)
        self.data_validation_view.update_table()
        self.data_validation_view.table.show()
        self.data_validation_view.show_view()


    def previous_error(self):
        #self.validate_data()
        if self.error_cursor>0:
            self.error_cursor-=1
        row= self.input_error_list.error_list[self.error_cursor][0] + 1
        column = self.input_error_list.error_list[self.error_cursor][1]
        self.data_validation_view.goto_row_column(row,column)
        #showinfo(title='Info', message="Previous error")

    def next_error(self):
        if self.error_cursor<len(self.input_error_list.error_list)-1:
            self.error_cursor+=1
        row= self.input_error_list.error_list[self.error_cursor][0] + 1
        column = self.input_error_list.error_list[self.error_cursor][1]
        self.data_validation_view.goto_row_column(row,column)
        #showinfo(title='Info', message="Next error")

    def recheck_data(self):
        self.validate_data()
        self.error_cursor=0
        row= self.input_error_list.error_list[self.error_cursor][0] + 1
        column = self.input_error_list.error_list[self.error_cursor][1]
        self.data_validation_view.goto_row_column(row,column)


    # def process_data(self):
    #     showinfo(title='Info', message="Start processing data")

    def process_data(self):
        self.data_validation_view.error_log.delete("1.0",tk.END)
        self.data_validation_view.error_log.insert(tk.INSERT,self.app_container.database.to_string())
        showinfo(title='Info', message="Start processing data")
        self.app_container.data_validation_controller.hide_view()
        self.app_container.report_generation_controller.show_view()
        self.app_container.report_generation_controller.generate_reports()
        # self.app_container.after(1,lambda:self.app_container.report_generation_controller.generate_reports())
        # import threading
        # self.app_container.after(1,lambda:threading.Thread(target=self.app_container.report_generation_controller.generate_reports()))
        # self.app_container.after(200,self.app_container.report_generation_controller.generate_reports())

    def test_one(self):
        self.data_validation_view.highlight_age_error(11)
        self.data_validation_view.highlight_age_error(22)
        self.data_validation_view.highlight_age_error(33)

    def test_two(self):
        self.data_validation_view.goto_row_column(11,'Age')