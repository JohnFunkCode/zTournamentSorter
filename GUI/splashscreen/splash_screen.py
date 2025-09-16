import logging
import tkinter as tk
from tkinter import ttk
from pathlib import Path

class SplashScreen(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # field options
        options = {'padx': 5, 'pady': 5}

        # data table label
        self.opening_label0 = ttk.Label(self, text='zUltimate Tournament App', font="Helvetica 22 bold")
        self.opening_label0.grid(column=0, row=0, **options)

        # Resolve image path relative to this file to avoid CWD issues
        image_path = Path(__file__).resolve().parent / 'zTournament_Colorado_1440x813.png'

        # Create the PhotoImage explicitly bound to this frame's master
        self.image = None
        try:
            if image_path.exists():
                self.image = tk.PhotoImage(master=self, file=str(image_path))
            else:
                logging.warning("Splash image not found at %s", image_path)
        except Exception as e:
            logging.exception("Failed to load splash image: %s", e)
            self.image = None

        # Keep a reference to the label (do not chain .grid())
        if self.image is not None:
            self.image_label = ttk.Label(self, image=self.image)
            self.image_label.grid(column=0, row=1, rowspan=2, **options)
        else:
            # Graceful fallback when image cannot be loaded
            self.image_label = ttk.Label(self, text='[ Splash image unavailable ]')
            self.image_label.grid(column=0, row=1, rowspan=2, **options)

    def show_view(self):
        self.grid()

    def hide_view(self):
        self.grid_forget()
