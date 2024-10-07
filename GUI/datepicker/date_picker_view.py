import logging
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime


class DatePickerView( tk.Toplevel):
    def __init__(self, app_container, controller):
        super().__init__(app_container)
        self.app_container = app_container
        self.controller=controller

        self.title("Date of the tournament?")

        # # field options
        # options = {'padx': 5, 'pady': 5}
        #
        # # add padding to the frame and show it
        # self.grid(**options)

        self.the_calendar = the_calendar = Calendar(self,
                                                    mindate=datetime(2020, 1, 1),
                                                    maxdate=datetime(2030, 1, 1),
                                                    showweeknumbers=False,
                                                    showothermonthdays=False,
                                                    foreground='red',
                                                    )
        self.the_calendar.bind("<<CalendarSelected>>", self.update_selected_date_button)
        self.the_calendar.grid()

        self.selected_date_button = tk.Button(self, text="Select Date", state="disabled",
                                              command=self.selected_date_clicked)
        self.selected_date_button.grid()
        # Modal window. - see: https://stackoverflow.com/questions/16803686/how-to-create-a-modal-dialog-in-tkinter
        # Wait for visibility or grab_set doesn't seem to work.
        self.wait_visibility()   # <<< NOTE
        self.grab_set()          # <<< NOTE
        self.transient(app_container)   # <<< NOTE

    def update_selected_date_button(self,event):
        self.selected_date_button.configure(text="Tournament Date: " + self.the_calendar.get_date(), state="active",
                                       background="DarkTurquoise")

    def selected_date_clicked(self):
        self.grab_release()      # <<< NOTE
        selected_date = self.the_calendar.selection_get()
        long_form_date_string = selected_date.strftime('%Y-%B-%d')
        logging.info(long_form_date_string)
        self.controller.date_selected(selected_date)
        self.destroy()

    def show_view(self):
        self.grid()

    def hide_view(self):
        self.grid_forget()