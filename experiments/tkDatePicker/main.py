# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

from pathlib import Path



class CalendarWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent=parent
        self.title("Calendar")

        self.the_calendar = the_calendar = Calendar(self,
                                                    mindate=datetime(2020, 1, 1),
                                                    maxdate=datetime(2030, 1, 1),
                                                    showweeknumbers=False,
                                                    showothermonthdays=False
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
        self.transient(parent)   # <<< NOTE

    def update_selected_date_button(self,event):

        self.selected_date_button.configure(text="Tournament Date: " + self.the_calendar.get_date(), state="active",
                                       command=self.selected_date_clicked,background="DarkTurquoise")
        #self.selected_date_button.grid()
        #try style as specified in this example to get the color to change
        #https: // www.reddit.com / r / learnpython / comments / m2z2ay / tkinter_button_background_wont_change_to_black /


    def selected_date_clicked(self):
        # turn off modal
        self.grab_release()      # <<< NOTE

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


def open_popup_calendar():
    print("Opening Popup Calendar")
    global popupCalendarWindow
    popupCalendarWindow = tk.Toplevel()
    popupCalendarWindow.wm_title("Calendar")

    global the_calendar
    the_calendar = Calendar(popupCalendarWindow,
                                 mindate=datetime(2020, 1, 1),
                                 maxdate=datetime(2030, 1, 1),
                                 showweeknumbers=False,
                                 showothermonthdays=False
                                 )
    the_calendar.bind("<<CalendarSelected>>", update_selected_date_button)
    the_calendar.pack()

    global selected_date_button
    selected_date_button = tk.Button(popupCalendarWindow, text="Select Date", state="disabled",
                                          command=selected_date_clicked)
    selected_date_button.pack()


def update_selected_date_button(event):
    selected_date_button.configure(text="Tournament Date: " + the_calendar.get_date(), state="active",
                                        background="DarkTurquoise")

def selected_date_clicked():
    # date = calendar.get_date()
    selected_date = the_calendar.selection_get()
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


# def setup_calendar():
# Use a breakpoint in the code line below to debug your script.

class Application(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.button_calendar = ttk.Button(self, text="Calendar", command=self.create_popup_calendar)
        self.button_calendar.grid()

    def create_popup_calendar(self):
        print("starting calendar")
        #open_popup_calendar()
        window=CalendarWindow(self)
        window.grab_set()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
