# Code to connect up the logging machanism to the list tkinter widget is based on the following pattern:
# https://stackoverflow.com/questions/10311755/how-to-direct-python-logger-to-tkinkers-listbox
# also see
# https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file

from logging import Handler, getLogger
import tkinter as tk
import tkinter.scrolledtext

class ListboxHandler(Handler):
    def __init__(self, box: tkinter.scrolledtext.ScrolledText):
        self._box = box
        Handler.__init__(self)

    def emit(self, record):
        r = self.format(record)
        self._box.insert(tk.INSERT, r + '\n')
        self._box.see(tk.INSERT)