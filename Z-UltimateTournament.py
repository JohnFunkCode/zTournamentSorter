# python
import tkinter as tk
from tkinter import font
import pandas as pd

import GUI.splashscreen.splash_screen
import GUI.menubar.menu_bar
import GUI.datavalidation.data_validation_controller
import GUI.reportgeneration.report_generation_controller
import GUI.datepicker.date_picker_controller
import GUI.filepicker.file_picker_controller


class zAppController(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('zUltimate App')
        self.geometry('1580x972')
        self.resizable(True, True)
        # macOS: .ico can raise; do not block startup if it fails
        try:
            self.iconbitmap("zultimate-logo_103x130-1.ico")
        except Exception:
            pass
        self.config(bg="Grey")

        new_font = font.nametofont("TkDefaultFont")
        new_font.config(family="Arial", size=14, weight="normal")

        # Global state
        self.ring_envelope_database_filename = ''
        self.input_data_filename = ''
        self.tournament_output_folder_path = ''
        self.database = pd.DataFrame()
        self.is_custom_division = False
        self.selected_date = None

        # Controllers
        self.menu_bar = GUI.menubar.menu_bar.MenuBar(self)
        self.report_generation_controller = GUI.reportgeneration.report_generation_controller.ReportGenerationController(self)
        self.data_validation_controller = GUI.datavalidation.data_validation_controller.DataValidationController(self)
        self.file_picker_controller = GUI.filepicker.file_picker_controller.FilePickerController(self)
        self.splash_screen = GUI.splashscreen.splash_screen.SplashScreen(self)
        self.date_picker_controller = GUI.datepicker.date_picker_controller.DatePickerController(self)

        # Initial UI
        self.report_generation_controller.hide_view()
        self.data_validation_controller.hide_view()
        self.splash_screen.show_view()

        # Start modal workflow once the window is ready
        # self.after_idle(self._open_date_picker_modal)
        self._open_date_picker_modal()

    def _open_date_picker_modal(self):
        parent = self
        modal = tk.Toplevel(parent)
        modal.title("Select Date")
        modal.transient(parent)
        modal.grab_set()

        container = tk.Frame(modal, bg="white")
        container.pack(fill="both", expand=True, padx=12, pady=12)

        # watch the confusing syntax - we're using a nested callback method
        def _on_date_selected(chosen_date):
            self.selected_date = chosen_date
            try:
                modal.grab_release()
            except Exception:
                pass
            modal.destroy()
            # Proceed to file picker after date modal closes
            self._open_file_picker_modal()

        self.date_picker_controller.show_it(container, on_complete=_on_date_selected)
        # Wait for the date modal to close; do not open file picker again here
        modal.wait_window(modal)

    def _go_to_data_validation(self):
        if hasattr(self.data_validation_controller, "set_selected_date"):
            self.data_validation_controller.set_selected_date(self.selected_date)
        self.data_validation_controller.show_view()

    def _open_file_picker_modal(self):
        # Let the controller manage its own modal Toplevel and grab

        # watch the confusing syntax - we're using a nested callback method
        def _on_files_selected(ring_path, reg_path):
            self.ring_envelope_database_filename = ring_path
            self.input_data_filename = reg_path
            self._go_to_data_validation()

        self.file_picker_controller.show_modal(self, on_complete=_on_files_selected)
        self.data_validation_controller.load_ring_envelope_database()
        self.data_validation_controller.load_tournament_file()
        self.splash_screen.hide_view()



if __name__ == "__main__":
    app = zAppController()
    app.mainloop()