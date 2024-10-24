import logging
import os
import pathlib
import time
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import pandas as pd

import webbrowser

import reports


class ReportGenerationView(ttk.Frame):
    def __init__(self, app_container, controller):
        super().__init__(app_container)
        self.app_container = app_container
        self.controller=controller

        # field options
        options = {'padx': 5, 'pady': 5}

        # add padding to the frame and show it
        self.grid(**options)

        # processing log label
        self.processing_log_label = ttk.Label(self, text='Processing Tournament Data')
        self.processing_log_label.grid(row=0, column=0, sticky=tk.W, **options)

        # processing log textbox
        self.processing_log_textbox = tk.scrolledtext.ScrolledText(self,width=201,height=40,wrap="none") # was width=212,height=43
        self.processing_log_textbox.grid(row=1, column=0, columnspan=3, **options)

        # button 1
        # self.process_data_button = ttk.Button(self, text='DoWork')
        # self.process_data_button['command'] = self.handle_button1
        # self.process_data_button.grid(row=0, column=1,sticky=tk.E, **options)

       # button 2
       #  self.process_data_button = ttk.Button(self, text='Show reports')
       #  self.process_data_button['command'] = self.handle_button2
       #  self.process_data_button.grid(row=0, column=2,sticky=tk.E, **options)

        # # self.final_output_labelframe.grid_forget()
        # i=0
        # for child in self.final_output_labelframe.winfo_children():
        #     if i!=0:
        #         child.grid_forget()
        #     i=i+1

    def show_view(self):
        self.grid()

    def hide_view(self):
        self.grid_forget()

    def show_final_reports(self):
        # field options
        options = {'padx': 5, 'pady': 5}

        # final output labelframe
        self.final_output_labelframe = ttk.LabelFrame(self, text='Final Ouput Files:')
        self.final_output_labelframe.grid(row=3, column=0, sticky=tk.W, **options)

        # Division Detail Report label
        if self.app_container.is_custom_division == False:
            self.division_detail_label = ttk.Label(self.final_output_labelframe, text='  division detail report.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
            self.division_detail_label.grid(row=1, column=0, sticky=tk.W, **options)
            # self.division_detail_label.bind('<Button-1>', lambda x: webbrowser.open("file://C:/Users/John/Documents/Tournaments/2023-April-30/DivisionDetailReport.pdf"))
            division_detail_report_filename_with_path='file://' + str(pathlib.Path(self.app_container.tournament_output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + 'DivisionDetailReport.pdf'))
            self.division_detail_label.bind('<Button-1>', lambda x: webbrowser.open(division_detail_report_filename_with_path))

        # Kata Detail Report label
        self.kata_score_sheet_lable = ttk.Label(self.final_output_labelframe, text='  kata score sheet.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
        self.kata_score_sheet_lable.grid(row=2, column=0, sticky=tk.W, **options)
        # self.kata_score_sheet_lable.bind('<Button-1>', lambda x: webbrowser.open("file://C:/Users/John/Documents/Tournaments/2023-April-30/KataScoreSheet.pdf"))
        kata_score_sheet_filename_with_path='file://' + str(pathlib.Path(self.app_container.tournament_output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + 'KataScoreSheet.pdf'))
        self.kata_score_sheet_lable.bind('<Button-1>', lambda x: webbrowser.open(kata_score_sheet_filename_with_path))

        # Technique Detail Report label
        if self.app_container.is_custom_division == False:
            self.technique_score_sheet_lable = ttk.Label(self.final_output_labelframe, text='  technique score sheet.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
            self.technique_score_sheet_lable.grid(row=3, column=0, sticky=tk.W, **options)
            # self.technique_score_sheet_lable.bind('<Button-1>', lambda x: webbrowser.open("file://C:/Users/John/Documents/Tournaments/2023-April-30/TechniqueScoreSheet.pdf"))
            technique_score_sheet_filename_with_path='file://' + str(pathlib.Path(self.app_container.tournament_output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + 'TechniqueScoreSheet.pdf'))
            self.technique_score_sheet_lable.bind('<Button-1>', lambda x: webbrowser.open(technique_score_sheet_filename_with_path))

        # Sparring Tree - letter report label
        self.sparring_tree_letter_size_label = ttk.Label(self.final_output_labelframe, text='  sparring tree - letter size.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
        self.sparring_tree_letter_size_label.grid(row=4, column=0, sticky=tk.W, **options)
        # self.sparring_tree_letter_size_label.bind('<Button-1>', lambda x: webbrowser.open("file://F:/Documents/Code/zTournamentSorter/SparringTreeReport-Legal.pdf"))
        sparring_tree_letter_filename_with_path='file://' + str(pathlib.Path(self.app_container.tournament_output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + 'SparringTreeReport-Letter.pdf'))
        self.sparring_tree_letter_size_label.bind('<Button-1>', lambda x: webbrowser.open(sparring_tree_letter_filename_with_path))

        # Sparring Tree - legal report label
        if self.app_container.is_custom_division == False:
            sparring_tree_legal_filename_with_path='file://' + str(pathlib.Path(self.app_container.tournament_output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + 'SparringTreeReport-Legal.pdf'))
            if os.path.exists(sparring_tree_legal_filename_with_path):
                self.sparring_tree_legal_size_label = ttk.Label(self.final_output_labelframe, text='  sparring tree - legal size.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
                self.sparring_tree_legal_size_label.grid(row=5, column=0, sticky=tk.W, **options)
                self.sparring_tree_legal_size_label.bind('<Button-1>', lambda x: webbrowser.open(sparring_tree_legal_filename_with_path))
            else:
                self.sparring_tree_legal_size_label = ttk.Label(self.final_output_labelframe, text='  sparring tree - legal size.pdf',font=('Helveticabold', 15), foreground="gray", cursor="hand2")
                self.sparring_tree_legal_size_label.grid(row=5, column=0, sticky=tk.W, **options)


            # self.sparring_tree_legal_size_label.bind('<Button-1>', lambda x: webbrowser.open("file://F:/Documents/Code/zTournamentSorter/SparringTreeReport-Letter.pdf"))

        # Tournament Summary report label
        if self.app_container.is_custom_division == False:
            self.tournament_summary_report_label = ttk.Label(self.final_output_labelframe, text='  tournament summary report.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
            self.tournament_summary_report_label.grid(row=6, column=0, sticky=tk.W, **options)
            # self.sparring_tree_legal_size_label.bind('<Button-1>', lambda x: webbrowser.open("file://F:/Documents/Code/zTournamentSorter/SparringTreeReport-Letter.pdf"))
            tournament_summary_report_filename_with_path='file://' + str(pathlib.Path(self.app_container.tournament_output_folder_path + reports.FileHandlingUtilities.pathDelimiter() + 'TournamentSummaryReport.pdf'))
            self.tournament_summary_report_label.bind('<Button-1>', lambda x: webbrowser.open(tournament_summary_report_filename_with_path))

        self.final_output_labelframe.grid()

    def show_final_reports_when_work_done(self,thread):
        # print("waiting for work to complete")
        time.sleep(5)
        while thread.is_alive():
            # print("still working")
            time.sleep(.5)
        # print("work is compleate")
        self.show_final_reports()


    def hide_final_reports(self):
        self.final_output_labelframe.grid_forget()
        pass

    def handle_button1(self):
        self.app_container.report_generation_controller.generate_reports()
        # self.hide_final_reports()
        pass

    def handle_button2(self):
        # self.controller.previous_error()
        self.show_final_reports()
        pass


