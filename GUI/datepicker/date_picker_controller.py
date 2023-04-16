from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import logging
from pathlib import Path
import GUI.datepicker.date_picker_view

class DatePickerController():
    def __init__(self, app_container: ttk.Frame):
        super().__init__()
        self.app_container = app_container
        self.date_picker_view = GUI.datepicker.date_picker_view.DatePickerView(app_container,self)

    def hide_view(self):
        self.date_picker_view.hide_view()

    def show_view(self):
        self.date_picker_view.show_view()


    def date_selected(self, selected_date: datetime):
        # use pathlib for all directory and file access
        # great tutorial at: https://towardsdatascience.com/dont-use-python-os-library-any-more-when-pathlib-can-do-141fefb6bdb5
        long_form_date_string = selected_date.strftime('%Y-%B-%d')
        logging.info(long_form_date_string)

        # get users home directory
        home_dir = Path.home()
        logging.info(f'home_dir={home_dir}')

        # create tournaments directory if needed
        # new_path = Path('~/Documents/Tournaments')
        # new_dir = new_path.expanduser()
        # Path(new_dir).mkdir(exist_ok=True)

        # create director for this date if needed
        new_path = Path('~/Documents/Tournaments/' + long_form_date_string)
        new_dir = new_path.expanduser()
        Path(new_dir).mkdir(exist_ok=True, parents=True)
        logging.info(f'new_dir={new_dir}')
        self.app_container.tournament_output_folder_path = str(new_dir)

        # write a test file to make sure everything works
        # new_path = Path('~/Documents/Tournaments/' + long_form_date_string + '/test.txt')
        # f = new_path.expanduser()
        # f.write_text(f'test file in {long_form_date_string} directory')
