# python
import tkinter as tk
from tkinter import ttk, font as tkfont
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
        self._apply_unified_theme()

        self.title('zUltimate App')
        # self.geometry('1580x972')
        self.geometry('1636x1126')
        self.resizable(True, True)
        # macOS: .ico can raise; do not block startup if it fails
        try:
            self.iconbitmap("zultimate-logo_103x130-1.ico")
        except Exception:
            pass

        # Global state
        self.ring_envelope_database_filename = ''
        self.input_data_filename = ''
        self.tournament_output_folder_path = None
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

    def _apply_unified_theme(self):
        """
        Apply a single cross‑platform ttk theme and normalize fonts & DPI scaling
        so the UI looks consistent on Windows and macOS.
        """
        # Force a neutral, cross-platform ttk theme
        style = ttk.Style(self)
        try:
            style.theme_use('clam')
        except Exception:
            # Fallback if clam is unavailable
            pass

        # Normalize the key Tk named fonts so ttk widgets inherit consistent typography
        base_size = 11  # adjust to taste (11–12 is a good cross-platform baseline)
        try:
            tkfont.nametofont("TkDefaultFont").configure(family="Segoe UI", size=base_size)
            tkfont.nametofont("TkTextFont").configure(family="Segoe UI", size=base_size)
            tkfont.nametofont("TkHeadingFont").configure(family="Segoe UI Semibold", size=base_size)
            tkfont.nametofont("TkFixedFont").configure(family="Cascadia Mono", size=base_size - 1)
        except Exception:
            # If some named fonts don't exist in this interpreter, ignore silently
            pass

        # Normalize DPI scaling across platforms (Tk uses 72pt per inch)
        try:
            px_per_inch = self.winfo_fpixels('1i')
            scaling = px_per_inch / 72.0
            # Many apps clamp to ~1.0–1.25 for visual parity; leave as-is for true DPI
            self.tk.call('tk', 'scaling', scaling)
        except Exception:
            pass

        # A couple of small style tweaks that often vary cross‑platform
        style.configure("TButton", padding=(10, 6))
        style.configure("Treeview", rowheight=int(2.0 * base_size))

        # Cross-platform hyperlink label styles (blue + underlined)
        base_ui_font = tkfont.nametofont("TkDefaultFont")
        hyperlink_font = base_ui_font.copy()
        try:
            hyperlink_font.configure(underline=1)
        except Exception:
            # If underline isn't supported, continue without failing
            pass
        style.configure("Hyperlink.TLabel", foreground="#0A66C2", font=hyperlink_font, cursor="hand2")
        style.map(
            "Hyperlink.TLabel",
            foreground=[("active", "#084E97"), ("pressed", "#063B73")],
            font=[("active", hyperlink_font), ("pressed", hyperlink_font)]
        )
        style.configure("DisabledHyperlink.TLabel", foreground="gray", font=base_ui_font)

    def _open_date_picker_modal(self):
        parent = self
        modal = tk.Toplevel(parent)
        modal.title("Select Date")
        modal.transient(parent)
        modal.grab_set()

        container = ttk.Frame(modal, padding=12)
        container.pack(fill="both", expand=True)

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
            # Now that header correction has finished, proceed
            self.data_validation_controller.load_ring_envelope_database()
            self.data_validation_controller.load_tournament_file()
            self.splash_screen.hide_view()

        self.file_picker_controller.show_modal(self, on_complete=_on_files_selected)
        # self.data_validation_controller.load_ring_envelope_database()
        # self.data_validation_controller.load_tournament_file()
        # self.splash_screen.hide_view()



if __name__ == "__main__":
    app = zAppController()
    app.mainloop()