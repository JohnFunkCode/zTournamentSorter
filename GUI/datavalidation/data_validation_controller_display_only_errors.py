import os
import sys
import logging
import pathlib
from shutil import copyfile
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd

import reports.FileHandlingUtilities
from GUI.listbox_log_handler import ListboxHandler
from cleaninput import cleaninput
from cleaninput import rename_colums as RN
from cleaninput import input_errors
import GUI.datavalidation.data_validation_view


class DataValidationController:
    def __init__(self, app_container: ttk.Frame):
        super().__init__()
        self.app_container = app_container
        self.data_validation_view = GUI.datavalidation.data_validation_view.DataValidationView(app_container, self)
        self.input_error_list = input_errors.InputErrors()
        self.error_cursor = 0
        self.displaying_errors_only = False
        self.error_row_indices = []
        self._orig_to_filtered_pos = {}
        self._full_dataset = None

    def hide_view(self):
        self.data_validation_view.hide_view()

    def show_view(self):
        self.data_validation_view.show_view()

    def load_tournament_file(self):
        working_file_name = self.app_container.input_data_filename
        path_to_selected_file = pathlib.Path(working_file_name).parent
        if path_to_selected_file != self.app_container.tournament_output_folder_path:
            tk.messagebox.showinfo(
                title='File Warning',
                message="The tournament data file isn't in the correct tournament folder. I'm copying it there."
            )
            source = pathlib.Path(working_file_name)
            destination = pathlib.Path(self.app_container.tournament_output_folder_path / source.name)
            copyfile(source, destination)
            working_file_name = str(destination)

        self.app_container.input_data_filename = working_file_name
        error_log_file_name = working_file_name[:-4] + "-ErrorLog.txt"

        logger = logging.getLogger('')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
        fh = logging.FileHandler(error_log_file_name)
        sh = logging.StreamHandler(sys.stdout)
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(sh)
        lh = ListboxHandler(self.data_validation_view.error_log)
        lh.setFormatter(formatter)
        logger.addHandler(lh)

        logging.info(" Reading the data from:" + self.app_container.input_data_filename + "....")

        try:
            cleaninput.clean_unicode_from_file(self.app_container.input_data_filename)
            r = RN.RenameColumns(self.app_container.input_data_filename)
            r.rename_all_columns()
            renamed_df = r.get_dataframe_copy()
            self.app_container.database = renamed_df
            self._full_dataset = renamed_df.copy()
            self.validate_data()
        except Exception as e:
            logging.error(f'Error loading file:{self.app_container.input_data_filename} \n {e}')

        self.data_validation_view.table.show()
        self.data_validation_view.show_view()

    def validate_data(self):
        working_df = self._full_dataset.copy() if self._full_dataset is not None else self.app_container.database

        self.input_error_list = input_errors.InputErrors()
        clean_df, _ = cleaninput.clean_all_input_errors(working_df, self.input_error_list)
        self._full_dataset = clean_df.copy()

        # Normalize & filter error indices
        self.input_error_list.error_list.sort()
        raw_error_rows = [row for row, _ in self.input_error_list.error_list]
        self.error_row_indices = sorted(set(raw_error_rows))

        valid_max = len(clean_df) - 1
        valid_rows = [r for r in self.error_row_indices if 0 <= r <= valid_max]

        if len(valid_rows) != len(self.error_row_indices):
            dropped = set(self.error_row_indices) - set(valid_rows)
            logging.warning(f'Dropped out-of-range error row indices (likely removed during cleaning): {sorted(dropped)}')
            # prune error_list to only valid rows
            self.input_error_list.error_list = [[r, c] for (r, c) in self.input_error_list.error_list if r in valid_rows]

        if valid_rows and self.input_error_list.error_list:
            # Build filtered view using positional indices safely
            try:
                filtered_df = clean_df.iloc[valid_rows].copy()
                self.app_container.database = filtered_df
                self.displaying_errors_only = True
                self._orig_to_filtered_pos = {orig: pos + 1 for pos, orig in enumerate(valid_rows)}  # 1-based
            except Exception as e:
                logging.error(f'Failed to build filtered error-only view: {e}. Falling back to full dataset.')
                self.app_container.database = clean_df
                self.displaying_errors_only = False
                self._orig_to_filtered_pos = {}
        else:
            # No valid errors
            self.app_container.database = clean_df
            self.displaying_errors_only = False
            self._orig_to_filtered_pos = {}
            self.data_validation_view.reset_color()

        self.data_validation_view.update_table()

        # Highlight errors
        if self.displaying_errors_only:
            for orig_row, col_name in self.input_error_list.error_list:
                disp = self._orig_to_filtered_pos.get(orig_row)
                if disp:
                    self._highlight_by_column(col_name, disp)
        else:
            for orig_row, col_name in self.input_error_list.error_list:
                self._highlight_by_column(col_name, orig_row + 1)

        logging.info(f'Input Errors:{self.input_error_list.error_list}')
        self.error_cursor = 0
        if self.input_error_list.error_list:
            self._goto_error_cursor()

    def _highlight_by_column(self, col_name, one_based_row):
        if col_name == 'Age':
            self.data_validation_view.highlight_age_error(one_based_row)
        elif col_name == 'Height':
            self.data_validation_view.highlight_height_error(one_based_row)
        elif col_name == 'Weight':
            self.data_validation_view.highlight_weight_error(one_based_row)
        elif col_name == 'Rank':
            self.data_validation_view.highlight_rank_error(one_based_row)

    def _goto_error_cursor(self):
        if not self.input_error_list.error_list:
            self.data_validation_view.goto_row_column(1, 'Registrant_ID')
            return
        try:
            orig_row, column = self.input_error_list.error_list[self.error_cursor]
        except IndexError:
            return
        if self.displaying_errors_only:
            display_row = self._orig_to_filtered_pos.get(orig_row)
        else:
            display_row = orig_row + 1
        if display_row:
            self.data_validation_view.goto_row_column(display_row, column)

    def previous_error(self):
        if self.error_cursor > 0:
            self.error_cursor -= 1
        self._goto_error_cursor()

    def next_error(self):
        if self.error_cursor < len(self.input_error_list.error_list) - 1:
            self.error_cursor += 1
        self._goto_error_cursor()

    def _merge_display_into_full(self):
        display_df = self.app_container.database
        if display_df is None:
            return
        if self._full_dataset is None:
            self._full_dataset = display_df.copy()
            return
        if self.displaying_errors_only:
            self._full_dataset.loc[display_df.index, display_df.columns] = display_df.values
        else:
            self._full_dataset = display_df.copy()

    def recheck_data(self):
        self._merge_display_into_full()
        self.app_container.database = self._full_dataset.copy()
        self.validate_data()

    def process_data(self):
        self._merge_display_into_full()
        input_path = pathlib.Path(self.app_container.input_data_filename)
        processed_filename = f"{input_path.stem}-Processed.csv"
        save_file_name = filedialog.asksaveasfilename(
            title='Save Data as...',
            initialdir=str(input_path.parent),
            initialfile=processed_filename,
            defaultextension='.csv',
            filetypes=[("csv", "*.csv")]
        )
        if save_file_name:
            logging.info(f"Saving processed file to {save_file_name}")
            to_save = self._full_dataset if self._full_dataset is not None else self.app_container.database
            pd.DataFrame(to_save).to_csv(save_file_name, index=False)
        else:
            logging.warning("Not saving processed file!")

        self.data_validation_view.error_log.delete("1.0", tk.END)
        full_display = self._full_dataset if self._full_dataset is not None else self.app_container.database
        self.data_validation_view.error_log.insert(tk.INSERT, full_display.to_string())
        self.app_container.data_validation_controller.hide_view()
        self.app_container.report_generation_controller.show_view()
        self.app_container.report_generation_controller.generate_reports()