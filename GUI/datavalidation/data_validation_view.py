import logging
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

        # # data table label
        # self.error_log_label = ttk.Label(self, text='Data Table')
        # self.error_log_label.grid(column=0, row=0, sticky=tk.W, **options)

        # pandas table
        self.pandas_table_frame = ttk.Frame(self,borderwidth=2,relief='sunken')
        self.table = Table(parent=self.pandas_table_frame, model=TableModel(app_container.database),
                           showtoolbar=False, showstatusbar=False, enable_menus=False, width=1550, height=551)
        self.pandas_table_frame.grid(row=1,column=0,rowspan=5, columnspan=3,**options)
        self.table.redraw()

        self.previous_button = ttk.Button(self, text='Previous Error')
        self.previous_button['command'] = self.handle_previous_button
        self.previous_button.grid(row=1, column=3,sticky=tk.W, **options)

        self.previous_button = ttk.Button(self, text='Next Error')
        self.previous_button['command'] = self.handle_next_button
        self.previous_button.grid( row=2, column=3, sticky=tk.W, **options)

        self.delete_button = ttk.Button(self, text='Delete Row')
        self.delete_button['command'] = self.handle_delete_button
        self.delete_button.grid(row=3, column=3, sticky=tk.W, **options)

        self.previous_button = ttk.Button(self, text='Re-Check Data')
        self.previous_button['command'] = self.handle_recheck_button
        self.previous_button.grid(row=4, column=3, sticky=tk.W, **options)

        # button 1
        self.process_data_button = ttk.Button(self, text='Process Data')
        self.process_data_button['command'] = self.process_data
        self.process_data_button.grid(row=5, column=3,sticky=tk.W, **options)


        # error log label
        self.error_log_label = ttk.Label(self, text='Data Errors')
        self.error_log_label.grid(row=6, column=0, sticky=tk.W, **options)

        # error log textbox
        self.error_log = tk.scrolledtext.ScrolledText(self,width=200,height=19,wrap="none")
        self.error_log.grid(row=7, column=0, columnspan=3, **options)


    def show_view(self):
        self.grid()

    def hide_view(self):
        self.grid_forget()

    def handle_previous_button(self):
        self.controller.previous_error()

    def handle_next_button(self):
        self.controller.next_error()

    def handle_delete_button(self):
        # self.table.show()
        # self.table.redraw()
        # self.table.movetoSelection(0,0)
        # self.table.redraw()

        r=self.table.getSelectedRow()
        self.table.deleteRow(ask=True)
        # self.controller.recheck_data()
        self.app_container.database = self.app_container.database= self.table.model.df
        self.controller.recheck_data()


    def handle_recheck_button(self):
        self.app_container.database= self.table.model.df
        self.controller.recheck_data()


    def process_data(self):
        self.controller.process_data()

    def update_table(self):
        self.table.updateModel(TableModel(self.app_container.database))

    def highlight_age_error(self, row_with_error):
        error_rows = range(row_with_error-1,row_with_error)
        age_column = self.table.model.df.columns.get_loc('Age')
        age_columns = range(age_column,age_column+1)
        self.table.setRowColors(rows=error_rows,clr='red',cols=age_columns)
        #self.table.redraw()

    def highlight_weight_error(self, row_with_error):
        error_rows = range(row_with_error-1,row_with_error)
        age_column = self.table.model.df.columns.get_loc('Weight')
        age_columns = range(age_column,age_column+1)
        self.table.setRowColors(rows=error_rows,clr='red',cols=age_columns)
        #self.table.redraw()


    def highlight_height_error(self, row_with_error):
        error_rows = range(row_with_error-1,row_with_error)
        age_column = self.table.model.df.columns.get_loc('Height')
        age_columns = range(age_column,age_column+1)
        self.table.setRowColors(rows=error_rows,clr='red',cols=age_columns)
        #self.table.redraw()

    def highlight_rank_error(self, row_with_error):
        error_rows = range(row_with_error-1,row_with_error)
        age_column = self.table.model.df.columns.get_loc('Rank')
        age_columns = range(age_column,age_column+1)
        self.table.setRowColors(rows=error_rows,clr='red',cols=age_columns)
        #self.table.redraw()

    def reset_color(self):
        all_rows = range(0,self.table.model.df.shape[0]-1)
        #all_columns = range(0,self.table.model.df.shape[1]-1)
        self.table.setRowColors(rows=all_rows,clr='white',cols='all')


    def goto_row_column(self,row, column_title):
        column_number = self.app_container.database.columns.get_loc(column_title)
        self.table.show()
        self.table.redraw()
        # self.table.setRowColors(rows=range(row-1,row),clr='red',cols=range(column_number-1,column_number))
        self.table.drawSelectedRect(row=row-1, col=column_number, color='red')
        self.table.movetoSelection(row=row-1, idx=column_title,offset=1) #was offet=7
        # self.table.currentrow=row
        # self.table.currentcol=column_number
        self.table.redraw()
        self.table.drawSelectedRect(row=row-1, col=column_number, color='red')

        # self.table.show()
        # self.redraw()
        # self.table.movetoSelection()
        # self.table.redraw()