import logging
import tkinter as tk
from tkinter import font

import GUI.splashscreen.splash_screen
import GUI.menubar.menu_bar
import GUI.datavalidation.data_validation_controller
import GUI.reportgeneration.report_generation_controller
import GUI.datepicker.date_picker_controller
import pandas as pd

class zAppController(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('zUltimate App')
        # self.geometry('1920x1080')
        # self.geometry('1721x972') original for Tournament Laptop
        # self.geometry('1440x900') best for macbook air default resolution
        self.geometry('1580x972')


        self.resizable(True, True)
        self.iconbitmap("zultimate-logo_103x130-1.ico")
        self.config(bg="Grey")  # self.config(bg="Light Grey")

        new_font = font.nametofont("TkDefaultFont")
        new_font.config(family="Arial", size=14, weight="normal")

        # a few globals from the old driver code
        self.ring_envelope_database_filename = ''  # the name of the ring envelope database file
        self.input_data_filename = ''  # the name of the input file - used in a lot of reports
        self.tournament_output_folder_path = '' # the path to all the ouput
        self.database = pd.DataFrame()
        self.is_custom_division = False # used to signal special processing if processing a custom division

        self.menu_bar = GUI.menubar.menu_bar.MenuBar(self)
        self.report_generation_controller = GUI.reportgeneration.report_generation_controller.ReportGenerationController(self)
        self.data_validation_controller=GUI.datavalidation.data_validation_controller.DataValidationController(self)
        self.splash_screen = GUI.splashscreen.splash_screen.SpashScreen(self)
        self.date_picker_controller = GUI.datepicker.date_picker_controller.DatePickerController(self)

        self.report_generation_controller.hide_view()
        self.data_validation_controller.hide_view()
        self.splash_screen.show_view()
        # self.date_picker_controller.show_view()


        # a few globals from the old driver code
        self.input_data_filename = ''   # the name of the input file - used in a lot of reports


if __name__ == "__main__":
    app = zAppController()
    app.mainloop()