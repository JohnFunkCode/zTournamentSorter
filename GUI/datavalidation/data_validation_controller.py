import os
import sys
import logging
import time
import pathlib
from shutil import copyfile

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from tkinter.messagebox import showinfo

import reports.FileHandlingUtilities
from GUI.listbox_log_handler import ListboxHandler

from cleaninput import cleaninput
from cleaninput import rename_colums as RN
from cleaninput import input_errors

import GUI.datavalidation.data_validation_view

from logging import Handler, getLogger



class DataValidationController():
    def __init__(self, app_container: ttk.Frame):
        super().__init__()
        self.app_container = app_container
        self.data_validation_view = GUI.datavalidation.data_validation_view.DataValidationView(app_container,self)
        self.input_error_list = input_errors.InputErrors()
        self.error_cursor = 0
        # self.errorLogFileName=''


    def hide_view(self):
        self.data_validation_view.hide_view()

    def show_view(self):
        self.data_validation_view.show_view()

    def load_tournament_file(self):
        # print(self.app_container.tournament_output_folder_path)
        working_file_name = filedialog.askopenfilename(title="Select the file with the tournament data",
                                                                            initialdir=self.app_container.tournament_output_folder_path,
                                                                            filetypes=[("csv","*.csv")])
        # if the input file isn't in the folder for the tournament date ask to move it.
        path_to_selected_file = str(pathlib.Path(working_file_name).parent)
        if path_to_selected_file != self.app_container.tournament_output_folder_path:
            tk.messagebox.showinfo(title='File Warning', message="That files isn't in the correct tournament folder. I'm copying it there." )
            source=pathlib.Path(working_file_name)
            # source_filename_only = source.name
            destination=pathlib.Path(self.app_container.tournament_output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + source.name )
            copyfile(source,destination)
            working_file_name=str(destination)

        self.app_container.input_data_filename = working_file_name

        errorLogFileName = self.app_container.input_data_filename[0:len(self.app_container.input_data_filename) - 4] + "-ErrorLog.txt"

        logger = logging.getLogger('')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(errorLogFileName)
        sh = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(sh)

        lh = ListboxHandler(self.data_validation_view.error_log)
        lh.setFormatter(formatter)
        logger.addHandler(lh)
        # logger.addHandler(ListboxHandler(self.data_validation_view.error_log))

        logging.info(" Reading the data from:" + self.app_container.input_data_filename + "....")

        try:
            cleaninput.clean_unicode_from_file(self.app_container.input_data_filename)

            # rename all the columns in the dataframe to usable names
            r = RN.RenameColumns(self.app_container.input_data_filename)
            r.rename_all_columns()
            renamed_df = r.get_dataframe_copy()
            self.app_container.database = renamed_df

            self.validate_data()
            # # self.input_error_list = input_errors.InputErrors()
            # clean_df,error_count=cleaninput.clean_all_input_errors(renamed_df, self.app_container.errorLogFile, self.input_error_list)
            # self.app_container.database =clean_df
            # self.data_validation_view.update_table()
            #
            # logging.info(f'Input Errors:{self.input_error_list.error_list}')
            # for i in range(len(self.input_error_list.error_list)):
            #     if self.input_error_list.error_list[i][1]=='Age':
            #         self.data_validation_view.highlight_age_error(self.input_error_list.error_list[i][0]+1)
            #     if self.input_error_list.error_list[i][1]=='Height':
            #         self.data_validation_view.highlight_weight_error(self.input_error_list.error_list[i][0]+1)
            #     if self.input_error_list.error_list[i][1]=='Weight':
            #         self.data_validation_view.highlight_weight_error(self.input_error_list.error_list[i][0]+1)
            #     if self.input_error_list.error_list[i][1] == 'Rank':
            #         self.data_validation_view.highlight_rank_error(self.input_error_list.error_list[i][0]+1)
            # self.input_error_list.error_list.sort()
        except Exception as e:
            logging.error(f'Error loading file:{self.app_container.input_data_filename} \n {e}')


        # self.app_container.errorLogFile.close()
        self.data_validation_view.table.show()
        self.data_validation_view.show_view()

        # TBD figure out how to goto the first error the first time the table is loaded - it appears the table isn't rendered yet.
        # row= self.input_error_list.error_list[self.error_cursor][0] + 1
        # column = self.input_error_list.error_list[self.error_cursor][1]
        # self.data_validation_view.goto_row_column(row,column)



    def validate_data(self):
        self.input_error_list = []
        self.input_error_list = input_errors.InputErrors()
        # self.data_validation_view.reset_color()

        # df=self.data_validation_view.table.model
        df = self.app_container.database
        clean_df,error_count= cleaninput.clean_all_input_errors(df, self.input_error_list)
        self.app_container.database =clean_df
        self.data_validation_view.update_table()

        self.input_error_list.error_list.sort()
        logging.info(f'Input Errors:{self.input_error_list.error_list}')
        for i in range(len(self.input_error_list.error_list)):
            if self.input_error_list.error_list[i][1]=='Age':
                self.data_validation_view.highlight_age_error(self.input_error_list.error_list[i][0]+1)
                # logging.info(f'Age:')

            if self.input_error_list.error_list[i][1]=='Height':
                self.data_validation_view.highlight_height_error(self.input_error_list.error_list[i][0]+1)
                # logging.info(f'Height:')

            if self.input_error_list.error_list[i][1]=='Weight':
                self.data_validation_view.highlight_weight_error(self.input_error_list.error_list[i][0]+1)
                # logging.info(f'Weight:')

            if self.input_error_list.error_list[i][1] == 'Rank':
                self.data_validation_view.highlight_rank_error(self.input_error_list.error_list[i][0]+1)
                # logging.info(f'Rank:')

        # logging.info('Start')
        #
        # self.data_validation_view.table.redraw()
        # self.data_validation_view.table.show()
        # self.data_validation_view.show_view()
        # logging.info('End')


    def load_division_file(self):
        self.is_custom_division=True
        # filename = filedialog.askopenfilename(title="Select the file with the division data",filetypes=[("csv","*.csv"),("excel","*.xls")])
        working_file_name = filedialog.askopenfilename(title="Select the file with the division data",
                                                                            initialdir=self.app_container.tournament_output_folder_path,
                                                                            filetypes=[("csv","*.csv"),("excel","*.xls")])
        # if the input file isn't in the folder for the tournament date ask to move it.
        path_to_selected_file = str(pathlib.Path(working_file_name).parent)
        if path_to_selected_file != self.app_container.tournament_output_folder_path:
            tk.messagebox.showinfo(title='File Warning', message="That files isn't in the correct tournament folder. I'm copying it there." )
            source=pathlib.Path(working_file_name)
            # source_filename_only = source.name
            destination=pathlib.Path(self.app_container.tournament_output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + source.name )
            copyfile(source,destination)
            working_file_name=str(destination)

        self.app_container.input_data_filename = working_file_name

        errorLogFileName = self.app_container.input_data_filename[0:len(self.app_container.input_data_filename) - 4] + "-ErrorLog.txt"

        logger = logging.getLogger('')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(errorLogFileName)
        sh = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(sh)

        lh = ListboxHandler(self.data_validation_view.error_log)
        lh.setFormatter(formatter)
        logger.addHandler(lh)
        # logger.addHandler(ListboxHandler(self.data_validation_view.error_log))

        logging.info(" Reading the data from:" + self.app_container.input_data_filename + "....")


        self.app_container.database = pd.read_csv(working_file_name)
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
        self.data_validation_view.reset_color()

        self.validate_data()

        logging.info('Start')
        self.data_validation_view.table.show()
        self.data_validation_view.table.redraw()
        self.data_validation_view.table.movetoSelection(0,0)
        self.data_validation_view.table.redraw()


        logging.info('End')

        self.error_cursor=0
        if len(self.input_error_list.error_list) >0 :
            row= self.input_error_list.error_list[self.error_cursor][0] + 1
            column = self.input_error_list.error_list[self.error_cursor][1]
            self.data_validation_view.goto_row_column(row,column)


    # def process_data(self):
    #     showinfo(title='Info', message="Start processing data")

    def process_data(self):
        # Save the database to file
        save_file_name = self.app_container.input_data_filename[0:len(self.app_container.input_data_filename) - 4] + "-Processed.csv"
        save_file_name=filedialog.asksaveasfilename(filetypes=[("csv","*.csv")],initialfile=save_file_name,title='Save Data as...')
        if(save_file_name != ''):
            logging.info(f"Saving processed file to {save_file_name}")
            df = pd.DataFrame(self.app_container.database)
            df.to_csv(save_file_name,index=False)
        else:
            logging.warning(f"Not saving processed file!")


        self.data_validation_view.error_log.delete("1.0",tk.END)
        self.data_validation_view.error_log.insert(tk.INSERT,self.app_container.database.to_string())
        # showinfo(title='Info', message="Start processing data")
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