# python
# File: GUI/datepicker/date_picker_view.py
import logging
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime


class DatePickerView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        self.root = ttk.Frame(parent)
        self.root.grid_columnconfigure(0, weight=1)

        self.the_calendar = Calendar(
            self.root,
            mindate=datetime(2020, 1, 1),
            maxdate=datetime(2030, 1, 1),
            showweeknumbers=False,
            showothermonthdays=False,
            foreground="red",
        )
        self.the_calendar.bind("<<CalendarSelected>>", self.update_selected_date_button)
        self.the_calendar.grid(row=0, column=0, padx=8, pady=8)

        self.selected_date_button = ttk.Button(
            self.root,
            text="Select Date",
            state="disabled",
            command=self.selected_date_clicked,
        )
        self.selected_date_button.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="e")

    def pack(self, **kwargs):
        self.root.pack(**kwargs)

    def grid(self, **kwargs):
        self.root.grid(**kwargs)

    def show_view(self):
        self.root.grid(row=0, column=0, sticky="nsew")
        self.root.tkraise()

    def hide_view(self):
        self.root.grid_remove()

    def update_selected_date_button(self, event=None):
        try:
            date_str = self.the_calendar.get_date()
            self.selected_date_button.configure(
                text=f"Tournament Date: {date_str}",
                state="normal",
            )
        except Exception:
            self.selected_date_button.configure(state="disabled")

    def selected_date_clicked(self):
        selected_date = self.the_calendar.selection_get()
        long_form_date_string = selected_date.strftime("%Y-%B-%d")
        logging.info(long_form_date_string)
        if hasattr(self.controller, "date_selected"):
            self.controller.date_selected(selected_date)