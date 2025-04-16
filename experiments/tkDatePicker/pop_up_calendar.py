from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

from pathlib import Path

class PopupCalendar:
    def __int__(self):
        self.asdf = 99
        print("initializing Popup Calendar")
        self.popupCalendarWindow = tk.Toplevel()
        self.popupCalendarWindow.wm_title("Calendar")

        self.the_calendar = Calendar(self.popupCalendarWindow,
                                     mindate=datetime(2020, 1, 1),
                                     maxdate=datetime(2030, 1, 1),
                                     showweeknumbers=False,
                                     showothermonthdays=False
                                     )
        self.the_calendar.bind("<<CalendarSelected>>", self.update_selected_date_button)
        self.the_calendar.pack()
        self.selected_date_button = tk.Button(self.popupCalendarWindow, text="Select Date", state="disabled",
                                              command=self.selected_date_clicked)
        self.selected_date_button.pack()

    def print_asdf(self):
        print(self.asdf)

    def update_selected_date_button(self, event):
        self.selected_date_button.configure(text="Tournament Date: " + self.the_calendar.get_date(), state="active",
                                            background="DarkTurquoise")

    def selected_date_clicked(self):
        # date = calendar.get_date()
        selected_date = self.the_calendar.selection_get()
        print(type(selected_date))
        # print("Tournament Date: " + selected_date)

        # use pathlib for all directory and file access
        # great tutorial at: https://towardsdatascience.com/dont-use-python-os-library-any-more-when-pathlib-can-do-141fefb6bdb5
        long_form_date_string = selected_date.strftime('%Y-%B-%d')
        print(long_form_date_string)

        # get users home directory
        home_dir = Path.home()
        print(f'home_dir={home_dir}')

        # create tournaments directory if needed
        # new_path = Path('~/Documents/Tournaments')
        # new_dir = new_path.expanduser()
        # Path(new_dir).mkdir(exist_ok=True)

        # create director for this date if needed
        new_path = Path('~/Documents/Tournaments/' + long_form_date_string)
        new_dir = new_path.expanduser()
        Path(new_dir).mkdir(exist_ok=True, parents=True)
        print(f'new_dir={new_dir}')

        new_path = Path('~/Documents/Tournaments/' + long_form_date_string + '/test.txt')
        f = new_path.expanduser()
        f.write_text(f'test file in {long_form_date_string} directory')

        root.quit()

if __name__ == '__main__':
  p = PopupCalendar()
  p.print_asdf()
