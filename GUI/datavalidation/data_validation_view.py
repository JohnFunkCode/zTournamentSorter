import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from pandastable import Table, TableModel

class DataValidationView(ttk.Frame):
    def __init__(self, app_container, controller):
        super().__init__(app_container)
        self.app_container = app_container
        self.controller=controller

        # field options
        options = {'padx': 5, 'pady': 5}

        # add padding to the frame and show it
        self.grid(**options)

        # data table label
        self.error_log_label = ttk.Label(self, text='Data Table')
        self.error_log_label.grid(column=0, row=0, sticky=tk.W, **options)

        # pandas table
        self.pandas_table_frame = ttk.Frame(self,borderwidth=2,relief='sunken')
        self.table = Table(parent=self.pandas_table_frame, model=TableModel(app_container.database),
                           showtoolbar=False, showstatusbar=False, enable_menus=False, width=1550, height=400)
        self.pandas_table_frame.grid(column=0,row=1,columnspan=3,**options)
        self.table.redraw()

        # error log label
        self.error_log_label = ttk.Label(self, text='Data Errors')
        self.error_log_label.grid(column=0, row=2, sticky=tk.W, **options)

        # error log textbox
        self.error_log = tk.scrolledtext.ScrolledText(self,width=200)
        self.error_log.grid(column=0, row=3, columnspan=3, **options)

        # button 1
        self.button_1 = ttk.Button(self, text='Process Data')
        self.button_1['command'] = self.process_data
        self.button_1.grid(column=3, row=4, sticky=tk.E, **options)

    def show_view(self):
        self.grid()

    def hide_view(self):
        self.grid_forget()

    def process_data(self):
        self.controller.process_data() ;

    def update_table(self):
        self.table.updateModel(TableModel(self.app_container.database))

    def highlight_age_error(self, row_with_error):
        error_rows = range(row_with_error-1,row_with_error)
        age_column = self.table.model.df.columns.get_loc('Age')
        age_columns = range(age_column,age_column+1)
        self.table.setRowColors(rows=error_rows,clr='red',cols=age_columns)
        self.table.redraw()

    def goto_row_column(self,row, column_title):
        column_number = self.app_container.database.columns.get_loc(column_title)
        self.table.movetoSelection(row=row-1, idx=column_title,offset=7)
        # self.table.currentrow=row
        self.table.currentcol=column_number
        self.table.redraw()
        self.table.drawSelectedRect(row=row-1, col=column_number, color='red')

