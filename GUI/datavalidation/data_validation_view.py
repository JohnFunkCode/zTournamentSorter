import logging
import tkinter as tk
from tkinter import ttk, font as tkfont
import tkinter.scrolledtext as scrolledtext
from pandastable import Table, TableModel

class DataValidationView(ttk.Frame):
    def __init__(self, app_container, controller):
        super().__init__(app_container, padding=12)
        self.app_container = app_container
        self.controller = controller

        # layout weights: table/log expand; button column fixed
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=0)
        self.rowconfigure(1, weight=1)  # table area
        self.rowconfigure(7, weight=1)  # error log area

        # field options
        options = {'padx': 8, 'pady': 8}

        # Title header (uses Title.TLabel from _apply_unified_theme)
        self.title_label = ttk.Label(self, text='Data Validation', style='Title.TLabel')
        self.title_label.grid(column=0, row=0, columnspan=4, sticky=tk.W, padx=4, pady=(0, 4))

        # # data table label
        # self.error_log_label = ttk.Label(self, text='Data Table')
        # self.error_log_label.grid(column=0, row=0, sticky=tk.W, **options)

        # pandas table
        self.pandas_table_frame = ttk.Frame(self, borderwidth=2, relief='sunken')
        # to show 25 lines we had the pandas table sized to 1211 x 551
        # current size is 1211 x 442 allows for 20 lines
        self.table = Table(parent=self.pandas_table_frame, model=TableModel(app_container.database),
                           showtoolbar=False, showstatusbar=False, enable_menus=False, width=1211, height=442)
        self.pandas_table_frame.grid(row=1, column=0, rowspan=5, columnspan=3, sticky="nsew", **options)
        self.table.redraw()

        # Remember default outline color so we can restore it
        self._default_box_outline = getattr(self.table, 'boxoutlinecolor', '#084B8A')
        # Whether we're programmatically moving to a cell (Next/Prev error, initial jump)
        self._programmatic_jump = False

        # --- Persistent red outline hook: reapply after any redraw/selection ---
        self._persist_red_outline = True
        self._orig_table_redraw = self.table.redraw
        self._orig_moveto = self.table.movetoSelection

        def _redraw_wrapper(event=None, callback=None):
            result = self._orig_table_redraw(event=event, callback=callback)
            try:
                if self._persist_red_outline and self.table.currentrow is not None and self.table.currentcol is not None:
                    self.table.boxoutlinecolor = 'red'
                    self.table.drawSelectedRect(row=self.table.currentrow, col=self.table.currentcol, color='red')
            except Exception:
                pass
            return result

        def _moveto_wrapper(*, row=None, col=None, idx=None, offset=0):
            try:
                result = self._orig_moveto(row=row, col=col, idx=idx, offset=offset)
            except TypeError:
                result = self._orig_moveto(row, col if col is not None else idx, offset)
            try:
                if getattr(self, '_lock_first_col_visible', False) and getattr(self, '_programmatic_jump', False):
                    self.table.set_xviews("moveto", 0)
            except Exception:
                pass
            try:
                final_row = row if row is not None else getattr(self.table, 'currentrow', None)
                final_col = col if col is not None else getattr(self.table, 'currentcol', None)
                if self._persist_red_outline and final_row is not None and final_col is not None:
                    self.table.boxoutlinecolor = 'red'
                    self.table.drawSelectedRect(row=final_row, col=final_col, color='red')
            except Exception:
                pass
            return result

        # Monkey-patch the table methods
        self.table.redraw = _redraw_wrapper
        self.table.movetoSelection = _moveto_wrapper

        # Keep first column visible by default
        self._lock_first_col_visible = True

        # Reapply red outline on visible-only redraws (e.g., scroll/resize)
        self._orig_redraw_visible = self.table.redrawVisible
        def _redraw_visible_wrapper(event=None, callback=None):
            result = self._orig_redraw_visible(event=event, callback=callback)
            try:
                if self._persist_red_outline and self.table.currentrow is not None and self.table.currentcol is not None:
                    self.table.boxoutlinecolor = 'red'
                    self.table.drawSelectedRect(row=self.table.currentrow, col=self.table.currentcol, color='red')
            except Exception:
                pass
            return result
        self.table.redrawVisible = _redraw_visible_wrapper

        # Reapply red outline after horizontal scroll
        self._orig_set_xviews = self.table.set_xviews
        def _set_xviews_wrapper(*args, **kwargs):
            result = self._orig_set_xviews(*args, **kwargs)
            try:
                if self._persist_red_outline and self.table.currentrow is not None and self.table.currentcol is not None:
                    self.table.boxoutlinecolor = 'red'
                    self.table.drawSelectedRect(row=self.table.currentrow, col=self.table.currentcol, color='red')
            except Exception:
                pass
            return result
        self.table.set_xviews = _set_xviews_wrapper

        # Reapply red outline after vertical scroll
        self._orig_set_yviews = self.table.set_yviews
        def _set_yviews_wrapper(*args, **kwargs):
            result = self._orig_set_yviews(*args, **kwargs)
            try:
                if self._persist_red_outline and self.table.currentrow is not None and self.table.currentcol is not None:
                    self.table.boxoutlinecolor = 'red'
                    self.table.drawSelectedRect(row=self.table.currentrow, col=self.table.currentcol, color='red')
            except Exception:
                pass
            return result
        self.table.set_yviews = _set_yviews_wrapper



        self.previous_button = ttk.Button(self, text='Previous Error')
        self.previous_button['command'] = self.handle_previous_button
        self.previous_button.grid(row=1, column=3,sticky=tk.W, **options)

        self.next_button = ttk.Button(self, text='Next Error')
        self.next_button['command'] = self.handle_next_button
        self.next_button.grid(row=2, column=3, sticky=tk.W, **options)

        self.delete_button = ttk.Button(self, text='Delete Row')
        self.delete_button['command'] = self.handle_delete_button
        self.delete_button.grid(row=3, column=3, sticky=tk.W, **options)

        self.recheck_button = ttk.Button(self, text='Re-Check Data')
        self.recheck_button['command'] = self.handle_recheck_button
        self.recheck_button.grid(row=4, column=3, sticky=tk.W, **options)

        # button 1
        self.process_data_button = ttk.Button(self, text='Process Data', state='disabled')
        self.process_data_button['command'] = self.process_data
        self.process_data_button.grid(row=5, column=3,sticky=tk.W, **options)

        # error log label
        self.error_log_label = ttk.Label(self, text='Data Errors')
        self.error_log_label.grid(row=6, column=0, sticky=tk.W, **options)

        # error log textbox (use scrolledtext module + unified font)
        # size was 181x18
        self.error_log = scrolledtext.ScrolledText(
            self, width=181, height=12, wrap="none",
            font=tkfont.nametofont("TkTextFont")
        )
        self.error_log.grid(row=7, column=0, columnspan=3, sticky="nsew", **options)

    def show_view(self):
        self.grid(sticky="nsew")

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
        self.table.redraw()

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
        all_rows = range(0, self.table.model.df.shape[0])
        # all_rows = range(0,self.table.model.df.shape[0]-1)
        #all_columns = range(0,self.table.model.df.shape[1]-1)
        self.table.setRowColors(rows=all_rows,clr='white',cols='all')

    def goto_row_column(self, row, column_title):
        column_number = self.app_container.database.columns.get_loc(column_title)
        # Convert incoming 1-based row to 0-based for pandastable
        target_row0 = max(0, row - 1)

        self.table.show()

        # Save the current outline color so we can restore it later
        old_outline_color = getattr(self.table, 'boxoutlinecolor', None)

        # Set outline color to red for error highlighting
        self.table.boxoutlinecolor = 'red'

        # Set pandastable's notion of the current cell
        self.table.currentrow = target_row0
        self.table.currentcol = column_number

        # Ensure geometry/col positions exist *before* movetoSelection to prevent IndexError
        # (retry patch applied)
        self.table.redraw()

        # Scroll into view and paint selection; use offset=0 for very first row
        scroll_offset = 0 if target_row0 == 0 else 1
        # Set programmatic jump flag before moving selection
        self._programmatic_jump = True
        try:
            self.table.movetoSelection(row=target_row0, col=column_number, offset=scroll_offset)
        except IndexError:
            # If positions weren't ready, redraw and try once more
            self.table.redraw()
            self.table.movetoSelection(row=target_row0, col=column_number, offset=scroll_offset)

        # Keep first column visible on initial jump using set_xviews (triggers redrawVisible)
        try:
            if getattr(self, '_lock_first_col_visible', False):
                self.table.set_xviews("moveto", 0)
        except Exception:
            pass
        finally:
            # Ensure subsequent user scrolls are not forced
            self._programmatic_jump = False

        # Ensure pending canvas operations are processed before custom overlay
        try:
            self.table.update_idletasks()
        except Exception:
            pass

        # Overlay a red rectangle to ensure visibility (especially row 0)
        self.table.drawSelectedRect(row=target_row0, col=column_number, color='red')

    # def goto_row_column(self,row, column_title):
    #     column_number = self.app_container.database.columns.get_loc(column_title)
    #     self.table.show()
    #     self.table.redraw()
    #     # self.table.setRowColors(rows=range(row-1,row),clr='red',cols=range(column_number-1,column_number))
    #     self.table.drawSelectedRect(row=row-1, col=column_number, color='red')
    #     self.table.movetoSelection(row=row-1, idx=column_title,offset=1) #was offet=7
    #     # self.table.currentrow=row
    #     # self.table.currentcol=column_number
    #     self.table.redraw()
    #     self.table.drawSelectedRect(row=row-1, col=column_number, color='red')
    #
    #     # self.table.show()
    #     # self.redraw()
    #     # self.table.movetoSelection()
    #     # self.table.redraw()
    def disable_error_highlighting(self):
        """Turn off persistent red outline and restore default outline color."""
        self._persist_red_outline = False
        try:
            self.table.boxoutlinecolor = getattr(self, '_default_box_outline', '#084B8A')
        except Exception:
            pass
        try:
            self.table.redraw()
        except Exception:
            pass

    def enable_error_highlighting(self):
        """Enable persistent red outline for error navigation/selection."""
        self._persist_red_outline = True
        try:
            self.table.boxoutlinecolor = 'red'
            self.table.redraw()
        except Exception:
            pass