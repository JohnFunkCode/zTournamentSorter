# python
from .date_picker_view import DatePickerView  # Adjust import as needed
from datetime import datetime
import logging
from pathlib import Path

class DatePickerController:
    def __init__(self, app_container):
        self.app = app_container
        self.parent = None
        self.on_complete = None
        self.view = None

    def show_it(self, parent, on_complete):
        self.parent = parent
        self.on_complete = on_complete
        self.view = DatePickerView(parent, controller=self)
        self.view.pack(fill="both", expand=True)

    def date_selected(self, selected_date):
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
        self.app.tournament_output_folder_path = str(new_dir)

        if callable(self.on_complete):
            self.on_complete(selected_date)
