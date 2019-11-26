import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
# from reportlab.rl_config import defaultPageSize


class SparringTreeReportPDF(object):
    def __init__(self):
        self.somvariable = 2


if __name__ == '__main__':
    '''test getting the number of SparringTree Report '''
