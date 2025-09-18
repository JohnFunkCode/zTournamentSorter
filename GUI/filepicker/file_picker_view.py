# python
# File: GUI/filepicker/file_picker_view.py
import os
from tkinter import ttk, filedialog
import tkinter as tk

class FilePickerView:
    def __init__(self, parent: ttk.Frame, controller):
        self.parent = parent
        self.controller = controller
        self.app_container = getattr(controller, "app_container", None)
        self._modal_top = None  # Set by controller if shown in a modal

        self.root = ttk.Frame(parent)
        self.root.grid_columnconfigure(2, weight=1)

        self.ring_file_var = tk.StringVar()
        self.reg_file_var = tk.StringVar()

        # Ring envelope picker
        ttk.Label(self.root, text="Ring envelope database:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.ring_btn = ttk.Button(self.root, text="Choose file...", command=self._pick_ring_file)
        # self.ring_btn = ttk.Button(self.root, text="Choose file...", command=controller.on_ring_file_chosen)

        self.ring_btn.grid(row=0, column=1, padx=8, pady=8, sticky="w")
        self.ring_entry = ttk.Entry(self.root, textvariable=self.ring_file_var, state="readonly")
        self.ring_entry.grid(row=0, column=2, padx=8, pady=8, sticky="ew")

        # Registration data picker
        ttk.Label(self.root, text="Registration data:").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.reg_btn = ttk.Button(self.root, text="Choose file...", command=self._pick_reg_file)
        # self.reg_btn = ttk.Button(self.root, text="Choose file...", command=controller.on_registration_file_chosen)
        self.reg_btn.grid(row=1, column=1, padx=8, pady=8, sticky="w")
        self.reg_entry = ttk.Entry(self.root, textvariable=self.reg_file_var, state="readonly")
        self.reg_entry.grid(row=1, column=2, padx=8, pady=8, sticky="ew")

        # Continue button (hidden until both files selected)
        self.continue_btn = ttk.Button(self.root, text="Continue to data validation", command=self._continue)
        self._hide_continue()

    def pack(self, **kwargs):
        self.root.pack(**kwargs)

    def grid(self, **kwargs):
        self.root.grid(**kwargs)

    def show_view(self):
        self.root.grid(row=0, column=0, sticky="nsew")
        self.root.tkraise()

    def hide_view(self):
        self.root.grid_remove()

    def set_modal_top(self, top: tk.Toplevel | None):
        """Controller can set the toplevel used for modal presentation so this view can close it on Continue."""
        self._modal_top = top

    def _pick_ring_file(self):
        initial_dir = getattr(self.app_container, "tournament_output_folder_path", os.getcwd())

        path = filedialog.askopenfilename(
            title="Select the file with the envelope database",
            initialdir=initial_dir,
            filetypes=[("csv", "*.csv"), ("All files", "*.*")]
        )
        if path:
            self.ring_file_var.set(path)
            if hasattr(self.controller, "on_ring_file_chosen"):
                self.controller.on_ring_file_chosen(path)
        self._update_continue_visibility()

    def _pick_reg_file(self):
        initial_dir = getattr(self.app_container, "tournament_output_folder_path", os.getcwd())
        path = filedialog.askopenfilename(
            title="Select the file with the tournament data",
            initialdir=initial_dir,
            filetypes=[("csv", "*.csv"), ("All files", "*.*")]
        )
        if path:
            self.reg_file_var.set(path)
            if hasattr(self.controller, "on_registration_file_chosen"):
                self.controller.on_registration_file_chosen(path)
        self._update_continue_visibility()

    def _update_continue_visibility(self):
        if self.ring_file_var.get() and self.reg_file_var.get():
            self._show_continue()
        else:
            self._hide_continue()

    def _show_continue(self):
        self.continue_btn.grid(row=3, column=0, columnspan=3, padx=8, pady=(16, 8), sticky="e")

    def _hide_continue(self):
        try:
            self.continue_btn.grid_remove()
        except Exception:
            pass

    def _continue(self):
        ring_path = self.ring_file_var.get()
        reg_path = self.reg_file_var.get()
        setattr(self.parent, "ring_envelope_database_filename", ring_path)
        setattr(self.parent, "input_data_filename", reg_path)

        if hasattr(self.controller, "on_continue"):
            self.controller.on_continue(ring_path, reg_path)
        # If we were shown modally, close the dialog
        if getattr(self, "_modal_top", None):
            try:
                self._modal_top.grab_release()
            except Exception:
                pass
            try:
                self._modal_top.destroy()
            except Exception:
                pass
            self._modal_top = None