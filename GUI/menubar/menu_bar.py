import tkinter as tk
from tkinter import messagebox

class MenuBar:
    def __init__(self, app_container):
        self.app_container = app_container
        menubar = tk.Menu()
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Full Tournament", command=self.open_tournament_file)
        filemenu.add_command(label="Open Custom Division", command=self.open_division_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=app_container.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.show_app_info)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # placeholder for testing
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Test One", command=self.test_one)
        helpmenu.add_command(label="Test Two", command=self.test_two)

        menubar.add_cascade(label="Test", menu=helpmenu)

        app_container.config(menu=menubar)

    def open_tournament_file(self):
        self.app_container.data_validation_controller.load_tournament_file()
        self.app_container.splash_screen.hide_view()

    def open_division_file(self):
        self.app_container.data_validation_controller.load_division_file()
        self.app_container.splash_screen.hide_view()

    def show_app_info(self):
        messagebox.showinfo("About", "Version beta 1\nLast updated 11/5/2022")

### framework for some tests
    def test_one(self):
        self.app_container.data_validation_controller.test_one()

    def test_two(self):
        # self.app_container.data_validation_controller.data_validation_view.goto_row_column(11,'Age')
        self.app_container.data_validation_controller.hide_view()
        self.app_container.splash_screen.hide_view()

        self.app_container.report_generation_controller.show_view()