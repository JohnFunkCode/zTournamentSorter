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

    def load_ring_envelope_database(self):
        # working_file_name = filedialog.askopenfilename(title="Select the file with the envelope database",
        #                                                                     initialdir=self.app_container.tournament_output_folder_path,
        #                                                                     filetypes=[("csv","*.csv")])
        working_file_name = self.app_container.ring_envelope_database_filename
        # if the ring envelope database file isn't in the folder for the tournament date let the user know we're copying it there.
        # path_to_selected_file = str(pathlib.Path(working_file_name).parent)
        path_to_selected_file = pathlib.Path(working_file_name).parent
        if path_to_selected_file != self.app_container.tournament_output_folder_path:
            tk.messagebox.showinfo(title='File Warning', message="The ring envelope database file isn't in the correct tournament folder. I'm copying it there." )
            source=pathlib.Path(working_file_name)
            # source_filename_only = source.name
            destination=pathlib.Path(self.app_container.tournament_output_folder_path / source.name )
            copyfile(source,destination)
            working_file_name=str(destination)

        self.app_container.ring_envelope_database_filename = working_file_name


    def load_tournament_file(self):
        # print(self.app_container.tournament_output_folder_path)
        # working_file_name = filedialog.askopenfilename(title="Select the file with the tournament data",
        #                                                                     initialdir=self.app_container.tournament_output_folder_path,
        #                                                                     filetypes=[("csv","*.csv")])
        working_file_name = self.app_container.input_data_filename
        # if the input file isn't in the folder for the tournament date let the user know we're copying it there.
        path_to_selected_file = pathlib.Path(working_file_name).parent
        if path_to_selected_file != self.app_container.tournament_output_folder_path:
            tk.messagebox.showinfo(title='File Warning', message="The tournament data file isn't in the correct tournament folder. I'm copying it there." )
            source=pathlib.Path(working_file_name)
            # source_filename_only = source.name
            destination=pathlib.Path(self.app_container.tournament_output_folder_path / source.name )
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

        # After initial render, highlight the first error (defer until idle so canvas is ready)
        if len(self.input_error_list.error_list) > 0:
            first_row = self.input_error_list.error_list[0][0]
            first_col = self.input_error_list.error_list[0][1]
            try:
                self.data_validation_view.after_idle(lambda: self.data_validation_view.goto_row_column(first_row, first_col))
            except Exception:
                pass



    def validate_data(self):
        self.input_error_list = []
        self.input_error_list = input_errors.InputErrors()
        # self.data_validation_view.reset_color()

        # df=self.data_validation_view.table.model
        df = self.app_container.database
        clean_df,error_count= cleaninput.clean_all_input_errors(df, self.input_error_list)
        # Ensure integer-like columns are actual integers so they don't render with decimal places
        int_like_cols = ['Registrant_ID']
        for col in int_like_cols:
            if col in clean_df.columns:
                clean_df[col] = pd.to_numeric(clean_df[col], errors='coerce').astype('Int64')
        self.app_container.database =clean_df
        self.data_validation_view.update_table()

        self.input_error_list.error_list.sort()
        logging.info(f'Input Errors:{self.input_error_list.error_list}')
        for i in range(len(self.input_error_list.error_list)):
            if self.input_error_list.error_list[i][1]=='Age':
                self.data_validation_view.highlight_age_error(self.input_error_list.error_list[i][0])  #was +1)
                # logging.info(f'Age:')

            if self.input_error_list.error_list[i][1]=='Height':
                self.data_validation_view.highlight_height_error(self.input_error_list.error_list[i][0])  #was +1)
                # logging.info(f'Height:')

            if self.input_error_list.error_list[i][1]=='Weight':
                self.data_validation_view.highlight_weight_error(self.input_error_list.error_list[i][0])  #was +1)
                # logging.info(f'Weight:')

            if self.input_error_list.error_list[i][1] == 'Rank':
                self.data_validation_view.highlight_rank_error(self.input_error_list.error_list[i][0])  #was +1)
                # logging.info(f'Rank:')

        # Keep the navigation cursor within bounds of the current error list
        errs = getattr(self.input_error_list, 'error_list', [])
        if errs:
            self.error_cursor = max(0, min(self.error_cursor, len(errs) - 1))
        else:
            self.error_cursor = 0

        if len(self.input_error_list.error_list) == 0:
            # No errors: clear any red cell colors and restore default outline
            self.data_validation_view.reset_color()
            self.data_validation_view.disable_error_highlighting()
        else:
            # There are errors: ensure the red outline persistence is enabled
            self.data_validation_view.enable_error_highlighting()


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
            destination=pathlib.Path(self.app_container.tournament_output_folder_path / source.name )
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


        self.app_container.database = pd.read_csv(working_file_name, keep_default_na=False)
        self.data_validation_view.update_table()
        self.data_validation_view.table.show()
        self.data_validation_view.show_view()

    def previous_error(self):
        errs = getattr(self.input_error_list, 'error_list', [])
        if not errs:
            showinfo(title='No Errors', message='There are no errors to navigate.')
            return
        # Move left if possible
        if self.error_cursor > 0:
            self.error_cursor -= 1
        else:
            # Already at the first error
            self.error_cursor = 0
            showinfo(title='Start of List', message='Already at the first error.')
            return
        try:
            row = errs[self.error_cursor][0]
            column = errs[self.error_cursor][1]
            self.data_validation_view.goto_row_column(row, column)
        except Exception:
            # Safety clamp
            self.error_cursor = max(0, min(self.error_cursor, len(errs) - 1))

    def next_error(self):
        errs = getattr(self.input_error_list, 'error_list', [])
        if not errs:
            showinfo(title='No Errors', message='There are no errors to navigate.')
            return
        # Move right if possible
        if self.error_cursor < len(errs) - 1:
            self.error_cursor += 1
        else:
            # Already at the last error
            self.error_cursor = len(errs) - 1
            showinfo(title='End of List', message='Already at the last error.')
            return
        try:
            row = errs[self.error_cursor][0]
            column = errs[self.error_cursor][1]
            self.data_validation_view.goto_row_column(row, column)
        except Exception:
            # Safety clamp
            self.error_cursor = max(0, min(self.error_cursor, len(errs) - 1))

    def recheck_data(self):
        self.data_validation_view.reset_color()

        # Disable Process Data button while checking
        self.data_validation_view.process_data_button.config(state='disabled')

        self.validate_data()

        logging.info('Start')
        self.data_validation_view.table.show()
        self.data_validation_view.table.redraw()

        errs = getattr(self.input_error_list, 'error_list', [])
        self.error_cursor = 0
        if errs:
            row = errs[self.error_cursor][0]
            column = errs[self.error_cursor][1]
            try:
                self.data_validation_view.after_idle(lambda: self.data_validation_view.goto_row_column(row, column))
            except Exception:
                self.data_validation_view.goto_row_column(row, column)
        else:
            # No errors remain; ensure cursor is reset
            self.error_cursor = 0
            tk.messagebox.showinfo(
                title='No More Errors',
                message='Good Job!  You fixed all the errors.  You may proceed to the next step.'
            )
            # Re-enable Process Data button now that validation passed
            # self.data_validation_view.process_data_button.config(state='normal')
            self.data_validation_view.process_data_button['state'] = 'normal'



        logging.info('End')

        # self.error_cursor=0
        # if len(self.input_error_list.error_list) >0 :
        #     row= self.input_error_list.error_list[self.error_cursor][0] # + 1
        #     column = self.input_error_list.error_list[self.error_cursor][1]
        #     self.data_validation_view.goto_row_column(row,column)


    # def process_data(self):
    #     showinfo(title='Info', message="Start processing data")

    def process_data(self):
        # Save the database to file
        #            destination=pathlib.Path(self.app_container.tournament_output_folder_path / source.name )
        # save_file_name = self.app_container.input_data_filename[0:len(self.app_container.input_data_filename) - 4] + "-Processed.csv"
        # save_file_name = pathlib.Path(self.app_container.input_data_filename[0:len(self.app_container.input_data_filename) - 4] / "-Processed.csv")
        input_path = pathlib.Path(self.app_container.input_data_filename)
        processed_filename = f"{input_path.stem}-Processed.csv"

        save_file_name = filedialog.asksaveasfilename(
            title='Save Data as...',
            initialdir=str(input_path.parent),
            initialfile=processed_filename,
            defaultextension='.csv',
            filetypes=[("csv", "*.csv")]
        )

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