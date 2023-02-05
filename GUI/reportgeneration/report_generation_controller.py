import logging
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from tkinter.messagebox import showinfo

import GUI.reportgeneration.report_generation_view

class ReportGenerationController():
    def __init__(self, app_container: ttk.Frame):
        super().__init__()
        self.app_container = app_container
        self.report_generation_view = GUI.reportgeneration.report_generation_view.ReportGenerationView(app_container,self)


    def hide_view(self):
        self.report_generation_view.hide_view()

    def show_view(self):
        self.report_generation_view.show_view()

    def generate_reports(self):
        import threading
        x=threading.Thread(target=self.dowork)
        logging.info("go")
        x.start()
        # self.app_container.after(500,lambda:x.start())
        #
        # x.start()
        # self.dowork()
        # self.report_generation_view.show_final_reports()
        # pass

    def dowork(self):
        for i in range(0,10):
            self.generate_reportline(i)
            # foo= lambda i:self.generate_reportline(i)
            # # foo(i)
            # self.app_container.after(500,foo,i)
            # foo= lambda i:self.generate_reportline(i)
            # foo(i)
        time.sleep(10)
        for i in range(10,100):
            self.generate_reportline(i)
            # foo= lambda i:self.generate_reportline(i)
            # # foo(i)
            # self.app_container.after(500,foo,i)
            # foo= lambda i:self.generate_reportline(i)
            # foo(i)
        self.report_generation_view.show_final_reports()


    def generate_reportline(self,i):
        # self.app_container.after(100,lambda:self.report_generation_view.processing_log_textbox.insert(tk.INSERT, f'processing {i}\n\r'))
        self.report_generation_view.processing_log_textbox.insert(tk.INSERT, f'processing {i}\n\r')
        logging.info(f'processing {i}')
        # time.sleep(1)

    def process_data(self):
        showinfo(title='Info', message="Start processing data")

    def test_one(self):
        pass
