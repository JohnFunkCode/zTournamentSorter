import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext

import webbrowser

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
        self.processing_log_textbox = tk.scrolledtext.ScrolledText(self,width=200,wrap="none")
        self.processing_log_textbox.grid(row=1, column=0, columnspan=3, **options)


        # # Output reports
        # self.final_output_label = ttk.Label(self, text='Final Ouput Reports:')
        # self.final_output_label.grid(row=2, column=0, sticky=tk.W, **options)
        #
        # # Output reports textbox
        # self.final_output_textbox = tk.Text(self, width=200, height=8, wrap="none")
        # self.final_output_textbox.grid(row=3, column=0, columnspan=3, **options)

        # # final output labelframe
        # self.final_output_labelframe = ttk.LabelFrame(self, text='Final Ouput Files:')
        # self.final_output_labelframe.grid(row=3, column=0, sticky=tk.W, **options)
        #
        # # Division Detail Report label
        # self.division_detail_label = ttk.Label(self.final_output_labelframe, text='  division detail report.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
        # self.division_detail_label.grid(row=1, column=0, sticky=tk.W, **options)
        # self.division_detail_label.bind('<Button-1>', lambda x: webbrowser.open("file://F:/Documents/Code/zTournamentSorter/DivisionDetailReport.pdf"))
        #
        # # Kata Detail Report label
        # self.kata_score_sheet_lable = ttk.Label(self.final_output_labelframe, text='  kata detail report.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
        # self.kata_score_sheet_lable.grid(row=2, column=0, sticky=tk.W, **options)
        # self.kata_score_sheet_lable.bind('<Button-1>', lambda x: webbrowser.open("file://F:/Documents/Code/zTournamentSorter/KataScoreSheet.pdf"))
        #
        # # Sparring Tree - letter report label
        # self.sparring_tree_letter_size_label = ttk.Label(self.final_output_labelframe, text='  sparring tree - letter size.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
        # self.sparring_tree_letter_size_label.grid(row=3, column=0, sticky=tk.W, **options)
        # self.sparring_tree_letter_size_label.bind('<Button-1>', lambda x: webbrowser.open("file://F:/Documents/Code/zTournamentSorter/SparringTreeReport-Legal.pdf"))
        #
        # # Sparring Tree - legal report label
        # self.sparring_tree_legal_size_label = ttk.Label(self.final_output_labelframe, text='  sparring tree - legal size.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
        # self.sparring_tree_legal_size_label.grid(row=4, column=0, sticky=tk.W, **options)
        # self.sparring_tree_legal_size_label.bind('<Button-1>', lambda x: webbrowser.open("file://F:/Documents/Code/zTournamentSorter/SparringTreeReport-Letter.pdf"))

        # button 1
        self.process_data_button = ttk.Button(self, text='DoWork')
        self.process_data_button['command'] = self.handle_button1
        self.process_data_button.grid(row=0, column=1,sticky=tk.E, **options)

       # button 2
        self.process_data_button = ttk.Button(self, text='Show reports')
        self.process_data_button['command'] = self.handle_button2
        self.process_data_button.grid(row=0, column=2,sticky=tk.E, **options)

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
        self.division_detail_label = ttk.Label(self.final_output_labelframe, text='  division detail report.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
        self.division_detail_label.grid(row=1, column=0, sticky=tk.W, **options)
        self.division_detail_label.bind('<Button-1>', lambda x: webbrowser.open("file://F:/Documents/Code/zTournamentSorter/DivisionDetailReport.pdf"))

        # Kata Detail Report label
        self.kata_score_sheet_lable = ttk.Label(self.final_output_labelframe, text='  kata detail report.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
        self.kata_score_sheet_lable.grid(row=2, column=0, sticky=tk.W, **options)
        self.kata_score_sheet_lable.bind('<Button-1>', lambda x: webbrowser.open("file://F:/Documents/Code/zTournamentSorter/KataScoreSheet.pdf"))

        # Sparring Tree - letter report label
        self.sparring_tree_letter_size_label = ttk.Label(self.final_output_labelframe, text='  sparring tree - letter size.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
        self.sparring_tree_letter_size_label.grid(row=3, column=0, sticky=tk.W, **options)
        self.sparring_tree_letter_size_label.bind('<Button-1>', lambda x: webbrowser.open("file://F:/Documents/Code/zTournamentSorter/SparringTreeReport-Legal.pdf"))

        # Sparring Tree - legal report label
        self.sparring_tree_legal_size_label = ttk.Label(self.final_output_labelframe, text='  sparring tree - legal size.pdf',font=('Helveticabold', 15), foreground="blue", cursor="hand2")
        self.sparring_tree_legal_size_label.grid(row=4, column=0, sticky=tk.W, **options)
        self.sparring_tree_legal_size_label.bind('<Button-1>', lambda x: webbrowser.open("file://F:/Documents/Code/zTournamentSorter/SparringTreeReport-Letter.pdf"))
        self.final_output_labelframe.grid()

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


