# python
import os
import pathlib
from tkinter import ttk, filedialog
import tkinter as tk

class FilePickerView:
    def __init__(self, parent: ttk.Frame, controller):
        self.parent = parent
        self.controller = controller
        self.app_container = getattr(controller, "app_container", None)
        self._modal_top = None

        # Store full paths separately (only filenames shown in UI)
        self._ring_full_path: str | None = None
        self._reg_full_path: str | None = None

        self.root = ttk.Frame(parent, padding=12)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=1)

        self.ring_file_var = tk.StringVar()
        self.reg_file_var = tk.StringVar()

        options = {"padx": 8, "pady": 8}
        self.title_label = ttk.Label(self.root, text="Select input files", style="Title.TLabel")
        self.title_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=4, pady=(0, 8))

        # Ring envelope picker
        ttk.Label(self.root, text="Ring envelope database:").grid(row=1, column=0, sticky="w", **options)
        self.ring_btn = ttk.Button(self.root, text="Choose file...", command=self._pick_ring_file)
        self.ring_btn.grid(row=1, column=1, sticky="w", **options)
        # Width large enough for "Tourn Ring Envelope Data Base_2025_05_03-proposed"
        self.ring_entry = ttk.Entry(self.root, textvariable=self.ring_file_var, state="readonly", width=54)
        self.ring_entry.grid(row=1, column=2, sticky="ew", **options)

        # Registration data picker
        ttk.Label(self.root, text="Registration data:").grid(row=2, column=0, sticky="w", **options)
        self.reg_btn = ttk.Button(self.root, text="Choose file...", command=self._pick_reg_file)
        self.reg_btn.grid(row=2, column=1, sticky="w", **options)
        self.reg_entry = ttk.Entry(self.root, textvariable=self.reg_file_var, state="readonly", width=54)
        self.reg_entry.grid(row=2, column=2, sticky="ew", **options)

        self.continue_btn = ttk.Button(self.root, text="Continue to fix headers", command=self._continue)
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
        self._modal_top = top

    def _pick_ring_file(self):
        initial_dir = getattr(self.app_container, "tournament_output_folder_path", None) or os.getcwd()
        try:
            initial_dir = str(pathlib.Path(initial_dir))
        except Exception:
            initial_dir = os.getcwd()
        if not os.path.isdir(initial_dir):
            initial_dir = os.getcwd()
        parent_win = self._modal_top if self._modal_top else self.root.winfo_toplevel()

        path = filedialog.askopenfilename(
            title="Select the file with the envelope database",
            initialdir=initial_dir,
            filetypes=[("csv", "*.csv"), ("All files", "*.*")],
            parent=parent_win
        )
        if path:
            self._ring_full_path = path
            self.ring_file_var.set(os.path.basename(path))
            if hasattr(self.controller, "on_ring_file_chosen"):
                self.controller.on_ring_file_chosen(path)
        self._update_continue_visibility()

    def _pick_reg_file(self):
        initial_dir = getattr(self.app_container, "tournament_output_folder_path", None) or os.getcwd()
        try:
            initial_dir = str(pathlib.Path(initial_dir))
        except Exception:
            initial_dir = os.getcwd()
        if not os.path.isdir(initial_dir):
            initial_dir = os.getcwd()
        parent_win = self._modal_top if self._modal_top else self.root.winfo_toplevel()

        path = filedialog.askopenfilename(
            title="Select the file with the tournament data",
            initialdir=initial_dir,
            filetypes=[("csv", "*.csv"), ("All files", "*.*")],
            parent=parent_win
        )
        if path:
            self._reg_full_path = path
            self.reg_file_var.set(os.path.basename(path))
            if hasattr(self.controller, "on_registration_file_chosen"):
                self.controller.on_registration_file_chosen(path)
        self._update_continue_visibility()

    def _update_continue_visibility(self):
        if self._ring_full_path and self._reg_full_path:
            self._show_continue()
        else:
            self._hide_continue()

    def _show_continue(self):
        self.continue_btn.grid(row=3, column=0, columnspan=3, sticky="e", padx=8, pady=(16, 8))

    def _hide_continue(self):
        try:
            self.continue_btn.grid_remove()
        except Exception:
            pass

    def _continue(self):
        ring_path = self._ring_full_path
        reg_path = self._reg_full_path
        setattr(self.parent, "ring_envelope_database_filename", ring_path)
        setattr(self.parent, "input_data_filename", reg_path)
        if hasattr(self.controller, "on_continue"):
            self.controller.on_continue(ring_path, reg_path)
        if self._modal_top:
            try:
                self._modal_top.grab_release()
            except Exception:
                pass
            try:
                self._modal_top.destroy()
            except Exception:
                pass
            self._modal_top = None
