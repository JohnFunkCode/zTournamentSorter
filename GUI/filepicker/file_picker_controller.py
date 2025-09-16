# python
# File: GUI/filepicker/file_picker_controller.py
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Callable
import logging

try:
    from GUI.filepicker.file_picker_view import FilePickerView
except Exception as e:
    raise ImportError("Could not import FilePickerView from GUI.filepicker.file_picker_view") from e


class FilePickerController:
    def __init__(self, app_container):
        """
        app_container: object holding shared state (e.g., attributes used elsewhere in the app)
        """
        self.app_container = app_container
        self.dialog = None
        self.view = None
        self.on_complete = None
        self._ring_path: Optional[str] = None
        self._reg_path: Optional[str] = None

    def show_modal(self, parent, on_complete: Optional[Callable[[str, str], None]] = None):
        """Open the FilePickerView as a modal dialog."""
        self.on_complete = on_complete
        self.dialog = tk.Toplevel(parent)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.title("Select Files")
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)

        container = tk.Frame(self.dialog, bg="white")
        container.pack(fill="both", expand=True, padx=12, pady=12)

        self.view = FilePickerView(container, controller=self)
        self.view.pack(fill="both", expand=True)

        self.dialog.wait_window(self.dialog)

    def _on_cancel(self):
        if self.dialog:
            try:
                self.dialog.grab_release()
            except Exception:
                pass
            self.dialog.destroy()

    def on_ring_file_chosen(self, path: str):
        if not self._is_valid_csv(path):
            messagebox.showerror("Invalid file", "Please pick a valid *.csv for the ring envelope database.")
            self.view.ring_file_var.set("")
            self._ring_path = None
            return

        print(f'Ring Envelope Database file is: {path}')
        logging.info(f'Ring Envelope Database file is: {path}')
        self._ring_path = path
        setattr(self.app_container, "ring_envelope_database_filename", path)
        setattr(self.app_container, "tournament_output_folder_path", os.path.dirname(path))

    def on_registration_file_chosen(self, path: str):
        if not self._is_valid_csv(path):
            messagebox.showerror("Invalid file", "Please pick a valid *.csv for the registration data.")
            self.view.reg_file_var.set("")
            self._reg_path = None
            return

        print(f'Registration Data file is: {path}')
        logging.info(f'Registration Data file is: {path}')
        self._reg_path = path
        setattr(self.app_container, "input_data_filename", path)
        setattr(self.app_container, "tournament_output_folder_path", os.path.dirname(path))

    def on_continue(self, ring_path: str, reg_path: str):
        if not self._is_valid_csv(ring_path):
            messagebox.showerror("Missing file", "The selected ring envelope database file is not accessible.")
            return
        if not self._is_valid_csv(reg_path):
            messagebox.showerror("Missing file", "The selected registration data file is not accessible.")
            return

        setattr(self.app_container, "ring_envelope_database_filename", ring_path)
        setattr(self.app_container, "input_data_filename", reg_path)

        if callable(self.on_complete):
            self.on_complete(ring_path, reg_path)

        self._close_modal()

    def _close_modal(self):
        if self.dialog:
            try:
                self.dialog.grab_release()
            except Exception:
                pass
            self.dialog.destroy()
            self.dialog = None

    @staticmethod
    def _is_valid_csv(path: str) -> bool:
        p = Path(path)
        return p.is_file() and p.suffix.lower() == ".csv"