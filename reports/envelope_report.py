"""
@author: john funk
"""
import logging
import pandas
import sys
import datetime
import time
import pathlib
from typing import Any

import pandas as pd
from reportlab.lib.pagesizes import letter, portrait, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdf_canvas

# import domain_model.constants as constants
import reports
import reports.FileHandlingUtilities


class EnvelopeReport():

    def __init__(self, title:str, data_file_name: str, output_folder_path:str):
        self.filename_with_path = f'{pathlib.Path(output_folder_path)}{reports.FileHandlingUtilities.pathDelimiter()}{"EnvelopeReport.pdf"}'
        # self.filename_with_path=str(pathlib.Path(output_folder_path + FileHandlingUtilities.reports.FileHandlingUtilities.pathDelimiter() +'EnvelopeReport.pdf')) #<--un-comment for stand alone test files

        # self.doc = SimpleDocTemplate("EnvelopeReport.pdf", pagesize=portrait(letter),topMargin=0, bottomMargin=0)
        self.canvas = pdf_canvas.Canvas(self.filename_with_path, pagesize=portrait(letter))

        #setup the package scoped global variables we need
        now = datetime.datetime.now()
        EnvelopeReport.timestamp = now.strftime("%Y-%m-%d %H:%M")
        # EnvelopeReport.sourcefile = "not initialized"
        EnvelopeReport.sourcefile = data_file_name
        EnvelopeReport.pageinfo = "not initialized"
        # EnvelopeReport.Title = "not
        EnvelopeReport.Title = title
        EnvelopeReport.PAGE_HEIGHT = 11 * inch
        EnvelopeReport.PAGE_WIDTH = 8.5 * inch
        EnvelopeReport.ring_number= "not initialized"
        EnvelopeReport.event_time= "not initialized"
        EnvelopeReport.division_name= "not initialized"
        EnvelopeReport.age= "not initialized"
        EnvelopeReport.belts= "not initialized"
        # EnvelopeReport.split_warning_text="not initialized"

    @staticmethod
    def set_title(title):
        EnvelopeReport.Title = title

    @staticmethod
    def set_pageInfo(pageinfo):
        EnvelopeReport.pageinfo = pageinfo

    @staticmethod
    def set_sourcefile(sourcefile):
        EnvelopeReport.sourcefile = sourcefile

    def add_division_details(self,event_time: str, division_name: str, division_type: str, gender: str, rank_label:str, minimum_age: int, maximum_age: int, rings: list, ranks:list, division_competitors: pandas.DataFrame):
        logging.info( f'division summary:{event_time} {division_name}  {division_type} {gender} {rank_label} {minimum_age} {maximum_age} {rings} {ranks}')
        logging.info( f'{division_competitors}')


    def add_summary_info_to_page(self, envelope_df: pandas.DataFrame):

        # Persist a debug snapshot for report-test repros without breaking PDF generation.
        try:
            path_for_report_test_data = pathlib.Path(__file__).resolve().parent / "report_test_data"
            path_for_report_test_data.mkdir(parents=True, exist_ok=True)
            envelope_df.to_pickle(path_for_report_test_data / "envelope_df.pkl")
        except OSError as exc:
            logging.warning("Unable to write envelope debug pickle: %s", exc)

        for _, row in envelope_df.iterrows():
            self._draw_envelope_page(row)
            self.canvas.showPage()

        return []

    def _draw_envelope_page(self, row: pandas.Series) -> None:
        x_position = 0.75 * inch
        line_height = 0.35 * inch
        box_padding = 0.2 * inch
        start_y = EnvelopeReport.PAGE_HEIGHT - x_position

        # self.canvas.setFont('Helvetica-Bold', 16)
        # self.canvas.drawString(x_position, start_y, EnvelopeReport.Title)
        #
        # self.canvas.setFont('Helvetica', 12)
        # self.canvas.drawRightString(
        #     EnvelopeReport.PAGE_WIDTH - x_position,
        #     start_y,
        #     f"Event Time: {row.get('Event_Time', '')}"
        # )

        current_y = start_y - 0.5 * inch
        # field_labels = [
        #     "Division",
        #     "Rank",
        #     "Age",
        #     "Last Name",
        #     "Ring #",
        #     "# Comp",
        #     "Center",
        #     "Corner",
        # ]
        # total_field_rows = len(field_labels)
        # box_height = total_field_rows * line_height + (2 * box_padding)
        # box_width = EnvelopeReport.PAGE_WIDTH - (2 * x_position) + (2 * box_padding)
        # self.canvas.roundRect(
        #     x_position - box_padding,
        #     current_y - box_height + box_padding,
        #     box_width,
        #     box_height,
        #     6,
        # )


        event_time = row.get("Event_Time", "")
        division_value = row.get("Division", "")
        rank_value = row.get("Rank", "")
        age_value = row.get("Age", "")
        last_name_range = row.get("Last Name", "")
        ring_number= row.get("Ring #", "")
        competitor_count = row.get("# Comp", "")
        center_value = row.get("Center", "")
        if center_value == "":
            center_value = " " * 20 # twenty spaces
        corner_value = row.get("Corner", "")
        if corner_value == "":
            corner_value = " " * 20 # twenty spaces

        self._draw_field_line(.5, .75, "Event Time", event_time)
        self._draw_field_line(4.75, .75, "Ring #", ring_number)
        self._draw_field_line(.25, 1.5, "Division", f'{division_value} ({age_value})')
        self._draw_field_line(.25, 2.25, "Rank", rank_value)
        self._draw_field_line(.25, 3, "Last Name Starting With", last_name_range)
        self._draw_field_line(.25, 3.75, "Participants", competitor_count)
        self._draw_field_line(.25, 4.5, "Comments", " " * 80)

        self._draw_field_line(5, 2, "Center", center_value)
        self._draw_field_line(5, 2.5, "Corner", corner_value)

        if "A-" in last_name_range:
            if not ("Z" in last_name_range):
                self._draw_field_line(5, 3, f'{last_name_range} Stays in Ring {ring_number}',"")

        underline = True
        no_underline = False
        # static instructions
        self._draw_instructions(.25,5.25,'Helvetica-Bold',15,no_underline,"Please")
        self._draw_instructions(1,5.26,'Helvetica',12,underline,"Print")
        self._draw_instructions(1.4,5.25,'Helvetica',12,no_underline,"names of the students and Dojos clearly.  DO NOT abbreviate.")
        self._draw_instructions(1, 5.5, 'Helvetica', 12, no_underline, "Bring participant patches to the ring to be handed out.")
        self._draw_instructions(1,5.75,'Helvetica',12,no_underline,"Bring winners to the head table to award trophies.")
        self._draw_instructions(1,6,'Helvetica',12,no_underline,"Have your paperwork done before you get to the head table.")
        #
        # # Places
        self._draw_instructions(.25,7,'Helvetica-Bold',15,no_underline,"1st Place")
        self._draw_instructions(1.25,7,'Helvetica',12,no_underline,"(name)")
        self._draw_instructions(1.9,7,'Helvetica',12,underline," " * 43)
        self._draw_instructions(4,7,'Helvetica',12,no_underline,"(studio)")
        self._draw_instructions(4.625,7,'Helvetica',12,underline," " * 45)

        self._draw_instructions(.25, 7.5, 'Helvetica-Bold', 15, no_underline, "2nd Place")
        self._draw_instructions(1.25, 7.5, 'Helvetica', 12, no_underline, "(name)")
        self._draw_instructions(1.9, 7.5, 'Helvetica', 12, underline, " " * 43)
        self._draw_instructions(4, 7.5, 'Helvetica', 12, no_underline, "(studio)")
        self._draw_instructions(4.625, 7.5, 'Helvetica', 12, underline, " " * 45)

        self._draw_instructions(.25, 8, 'Helvetica-Bold', 15, no_underline, "3rd Place")
        self._draw_instructions(1.25, 8, 'Helvetica', 12, no_underline, "(name)")
        self._draw_instructions(1.9, 8, 'Helvetica', 12, underline, " " * 43)
        self._draw_instructions(4, 8, 'Helvetica', 12, no_underline, "(studio)")
        self._draw_instructions(4.625, 8, 'Helvetica', 12, underline, " " * 45)

        self._draw_instructions(.25, 8.5, 'Helvetica-Bold', 15, no_underline, "4th Place")
        self._draw_instructions(1.25, 8.5, 'Helvetica', 12, no_underline, "(name)")
        self._draw_instructions(1.9, 8.5, 'Helvetica', 12, underline, " " * 43)
        self._draw_instructions(4, 8.5, 'Helvetica', 12, no_underline, "(studio)")
        self._draw_instructions(4.625, 8.5, 'Helvetica', 12, underline, " " * 45)

        self._draw_footer()


    def _draw_instructions(self, x_position: float, y_position: float, font: str, size: float, underline: bool, text: str) -> None:
        adjusted_x = x_position * inch
        adjusted_y = EnvelopeReport.PAGE_HEIGHT - (y_position * inch)

        self.canvas.setFont(font, size)
        self.canvas.drawString(adjusted_x, adjusted_y, text)


        if underline:
            underline_y = adjusted_y - 0.03 * inch
            underline_width = self.canvas.stringWidth(text, font, size)
            self.canvas.setLineWidth(0.5)
            self.canvas.line(adjusted_x, underline_y, adjusted_x + underline_width, underline_y)

    def _draw_footer(self) -> None:
        self.canvas.setFont('Times-Roman', 9)
        footer_y = 0.4 * inch
        self.canvas.drawCentredString(
            EnvelopeReport.PAGE_WIDTH / 2.0,
            footer_y,
            "Generated: %s   From file: %s" % (EnvelopeReport.timestamp, EnvelopeReport.sourcefile)
        )


    def write_pdfpage(self):
        self.canvas.save()

    def _draw_field_line(self, x_position: float, y_position: float, label: str, value: Any) -> None:
        adjusted_x = x_position * inch
        adjusted_y = EnvelopeReport.PAGE_HEIGHT - y_position * inch
        self.canvas.setFont('Helvetica-Bold', 18)
        if label == "":
            label_text = ""
        else:
            label_text = f"{label}"
        self.canvas.drawString(adjusted_x, adjusted_y, label_text)
        label_width = self.canvas.stringWidth(label_text, 'Helvetica-Bold', 18)

        value_text = "" if value is None else str(value)
        self.canvas.setFont('Helvetica', 18)
        value_x = adjusted_x + label_width + 0.15 * inch
        self.canvas.drawString(value_x, adjusted_y, value_text)

        if value_text:
            underline_y = adjusted_y - 0.05 * inch
            value_width = self.canvas.stringWidth(value_text, 'Helvetica', 18)
            self.canvas.setLineWidth(0.5)
            self.canvas.line(value_x, underline_y, value_x + value_width, underline_y)


def page_layout(canvas, doc):
    # (Unused with direct canvas drawing, kept for compatibility)
    pass



def _normalize_sample_envelope_data(sample_data: dict[str, list[Any]]) -> dict[str, list[Any]]:
    """
    Keep all sample columns the same length before creating a DataFrame.
    This data is manually edited and can drift out of sync over time.
    """
    lengths = {column: len(values) for column, values in sample_data.items()}
    unique_lengths = set(lengths.values())
    if len(unique_lengths) <= 1:
        return sample_data

    target_length = max(unique_lengths)
    logging.warning(
        "Envelope sample data has uneven column lengths; padding to %d rows. Lengths: %s",
        target_length,
        lengths,
    )
    fill_defaults: dict[str, Any] = {"# Comp": 0, "Center": "", "Corner": ""}

    normalized_data: dict[str, list[Any]] = {}
    for column, values in sample_data.items():
        padded_values = list(values)
        if len(padded_values) < target_length:
            padded_values.extend([fill_defaults.get(column, "")] * (target_length - len(padded_values)))
        normalized_data[column] = padded_values[:target_length]
    return normalized_data


def main():
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("EnvelopeReport.log")
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s', datefmt='%H:%M:%S')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    TSR_pdf = EnvelopeReport("Envelope Report", "DataFileName", "")

    # read test data from the pickle file at /Users/johnfunk/Documents/code/zTournamentSorter/reports/report_test_data/envelope_df.pkl
    # envelope_df = pd.read_pickle(pathlib.Path(__file__).resolve().parent / "report_test_data" / "envelope_df.pkl")

    envelope_data = {
        'Event_Time': ['9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:00 a.m.',
                       '9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:00 a.m.', '9:45 a.m.',
                       '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.',
                       '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.', '9:45 a.m.',
                       '9:45 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.',
                       '10:30 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.', '10:30 a.m.',
                       '10:30 a.m.', '10:30 a.m.', '11:15 a.m.', '11:15 a.m.', '11:15 a.m.', '11:15 a.m.', '11:15 a.m.', '11:15 a.m.', '11:15 a.m.',
                       '11:15 a.m.', '11:15 a.m.', '11:15 a.m.', '11:15 a.m.', '11:15 a.m.', '11:15 a.m.', '11:15 a.m.', '11:15 a.m.', '11:15 a.m.',
                       '11:15 a.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.',
                       '1:30 p.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.', '1:30 p.m.',
                       '1:30 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.',
                       '2:15 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.', '2:15 p.m.',
                       '2:15 p.m.', '2:15 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.',
                       '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.',
                       '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:00 p.m.', '3:45 p.m.', '3:45 p.m.', '3:45 p.m.', '3:45 p.m.',
                       '3:45 p.m.', '3:45 p.m.', '3:45 p.m.', '3:45 p.m.', '3:45 p.m.', '3:45 p.m.', '3:45 p.m.', '3:45 p.m.', '3:45 p.m.',
                       '3:45 p.m.', '3:45 p.m.', '3:45 p.m.', '3:45 p.m.', '3:45 p.m.', '12:00 noon', '12:00 noon', '12:00 noon', '4:15 p.m.',
                       '4:15 p.m.', '4:15 p.m.', '4:15 p.m.', '4:15 p.m.', '4:15 p.m.', '4:15 p.m.'],
        'Division': ['Kids Kata', 'Kids Kata', 'Kids Kata', 'Kids Kata', 'Kids Kata', 'Youth Techniques', 'Youth Techniques', 'Youth Techniques',
                     'Youth Techniques', 'Youth Techniques', 'Youth Techniques', 'Youth Techniques', "Girl's Sparring", "Girl's Sparring",
                     "Girl's Sparring", "Girl's Sparring", "Girl's Sparring", 'Kids Sparring', 'Kids Sparring', 'Kids Sparring', 'Kids Sparring',
                     'Kids Sparring', 'Kids Sparring', 'Kids Sparring', 'Kids Sparring', 'Youth Boys Sparring', 'Youth Boys Sparring',
                     'Youth Boys Sparring', 'Youth Boys Sparring', 'Youth Boys Sparring', 'Youth Boys Sparring', 'Youth Boys Sparring',
                     'Youth Boys Sparring', 'Youth Boys Sparring', 'Youth Boys Sparring', 'Youth Boys Sparring', 'Youth Boys Sparring',
                     'Boys & Girls Techniques', 'Boys & Girls Techniques', 'Boys & Girls Techniques', 'Boys & Girls Techniques',
                     'Boys & Girls Techniques', 'Boys & Girls Techniques', 'Boys & Girls Techniques', 'Boys & Girls Techniques', 'Kids Techniques',
                     'Kids Techniques', 'Kids Techniques', 'Kids Techniques', 'Kids Techniques', 'Kids Techniques', 'Kids Techniques',
                     'Youth Girls Sparring', 'Youth Girls Sparring', 'Youth Girls Sparring', 'Youth Girls Sparring', 'Boys & Girls Kata',
                     'Boys & Girls Kata', 'Boys & Girls Kata', 'Boys & Girls Kata', 'Boys & Girls Kata', 'Boys & Girls Kata', 'Boys & Girls Kata',
                     'Boys & Girls Kata', 'Boys & Girls Kata', 'Boys & Girls Kata', 'Boys & Girls Kata', 'Boys & Girls Kata', 'Youth Kata',
                     'Youth Kata', 'Youth Kata', 'Youth Kata', 'Youth Kata', "Boy's Sparring", "Boy's Sparring", "Boy's Sparring", "Boy's Sparring",
                     "Boy's Sparring", "Boy's Sparring", "Boy's Sparring", "Boy's Sparring", "Boy's Sparring", "Boy's Sparring", "Boy's Sparring",
                     "Boy's Sparring", "Boy's Sparring", "Boy's Sparring", "Boy's Sparring", "Boy's Sparring", "Boy's Sparring",
                     'Teen Girls Sparring', 'Teen Girls Sparring', 'Teen Girls Sparring', 'Teen Girls Sparring', 'Teen Girls Sparring',
                     'Teen Girls Sparring', 'Teen Girls Sparring', 'Teen Girls Sparring', 'Teen Girls Sparring', 'Teen Girls Sparring',
                     'Teen Girls Sparring', 'Teen Girls Sparring', 'Teen Girls Sparring', 'Teen Girls Sparring', 'Teen Girls Sparring',
                     'Teen Girls Sparring', 'Teen Girls Sparring', 'Teen Girls Sparring', 'Teen Girls Sparring', "Young Adult Men's Sparring",
                     "Young Adult Men's Sparring", "Young Adult Men's Sparring", "Young Adult Men's Sparring", "Young Adult Men's Sparring",
                     "Young Adult Men's Sparring", "Young Adult Men's Sparring", "Young Adult Men's Sparring", "Young Adult Men's Sparring",
                     "Young Adult Men's Sparring", "Young Adult Men's Sparring", "Young Adult Men's Sparring", "Young Adult Men's Sparring",
                     "Young Adult Men's Sparring", "Young Adult Men's Sparring", "Young Adult Men's Sparring", "Young Adult Men's Sparring",
                     "Young Adult Men's Sparring", "Young Adult Men's Sparring", "Young Adult Men's Sparring", "Young Adult Men's Sparring",
                     'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata',
                     'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata',
                     'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata', 'Men & Women Kata',
                     'Senior Techniques', 'Senior Techniques', 'Senior Techniques', 'Teen Boys Sparring', 'Teen Boys Sparring', 'Teen Boys Sparring',
                     'Teen Boys Sparring', 'Teen Boys Sparring', 'Teen Boys Sparring', 'Teen Boys Sparring'],
        'Rank': ['White', 'Yellow', 'Orange', 'Purple, Blue, Blue w/Stripe', 'Green, Green w/Stripe, Brown', 'White, Yellow, Orange', 'Purple ',
                 'Blue, Blue w/Stripe', 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White, Yellow', 'Orange', 'Purple', 'Blue, Blue w/Stripe',
                 'Green, Green w/Stripe', 'Brown', 'Jr. Black & Black', 'White', 'Yellow', 'Orange', 'Purple, Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White, Yellow', 'Purple ', 'White, Yellow, Orange', 'Purple', 'Blue, Blue w/Stripe',
                 'Green, Green w/Stripe', 'Brown', 'Jr. Black & Black', 'White', 'Yellow', 'Orange', 'Purple, Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White', 'Yellow', 'Orange', 'Purple, Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White, Yellow', 'Purple ', 'White', 'Yellow', 'Orange', 'Purple, Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White, Yellow', 'White, Yellow, Orange', 'Purple', 'Blue, Blue w/Stripe',
                 'Green, Green w/Stripe', 'White', 'Yellow', 'Orange', 'Purple, Blue, Blue w/Stripe', 'Green, Green w/Stripe, Brown', 'Jr. Black',
                 'White, Yellow', 'Purple ', 'Blue, Blue w/Stripe', 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White, Yellow', 'Purple',
                 'Blue, Blue w/Stripe', 'Green, Green w/Stripe', 'Brown', 'Jr. Black & Black', 'White', 'Yellow', 'Orange',
                 'Purple, Blue, Blue w/Stripe', 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White, Yellow', 'Purple ', 'Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Brown', 'Jr. Black & Black', 'White', 'Yellow', 'Orange', 'Purple, Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White - Jr. Black', 'Black', 'White, Yellow, Orange', 'Purple', 'Blue, Blue w/Stripe',
                 'Green, Green w/Stripe', 'Brown', 'Jr. Black & Black', 'White', 'Yellow', 'Orange', 'Purple, Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White - Jr. Black', 'Black', 'White, Yellow', 'Purple ', 'Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Brown', 'Jr. Black & Black', 'White', 'Yellow', 'Orange', 'Purple, Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White - Jr. Black', 'Black', 'White, Yellow', 'Purple ', 'Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Brown', 'Jr. Black & Black', 'White', 'Yellow', 'Orange', 'Purple, Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White, Yellow', 'Purple ', 'Blue, Blue w/Stripe', 'Green - Jr. Black', 'Black',
                 'White, Yellow', 'Orange', 'Purple, Blue, Blue w/Stripe', 'Green, Green w/Stripe ', 'Jr. Black', 'White - Jr. Black', 'Black',
                 'White - Blue w/Green Stripe', 'Green - Jr. Black', 'Black', 'White, Yellow, Orange', 'Purple, Blue, Blue w/Stripe',
                 'Green, Green w/Stripe, Brown', 'Jr. Black', 'White - Jr. Black', 'Black'],
        'Age': ['4-6', '4-6', '4-6', '4-6', '4-6', '7-8', '7-8', '7-8', '7-8', '7-8', '9-11', '9-11', '12-14', '12-14', '12-14', '12-14', '12-14',
                '4-6', '4-6', '4-6', '4-6', '4-6', '4-6', '4-6', '4-6', '7-8', '7-8', '7-8', '7-8', '7-8', '7-8', '9-11', '9-11', '9-11', '9-11',
                '9-11', '9-11', '4-6', '4-6', '4-6', '4-6', '4-6', '4-6', '7-8', '7-8', '4-6', '4-6', '4-6', '4-6', '4-6', '4-6', '4-6', '7-8', '7-8',
                '7-8', '7-8', '4-6', '4-6', '4-6', '4-6', '4-6', '4-6', '7-8', '7-8', '7-8', '7-8', '7-8', '7-8', '7-8', '9-11', '9-11', '9-11',
                '9-11', '9-11', '12-14', '12-14', '12-14', '12-14', '12-14', '12-14', '12-14', '12-14', '12-14', '12-14', '12-14', '12-14', '12-14',
                '12-14', '12-14', '12-14', '12-14', '15-17', '15-17', '15-17', '15-17', '15-17', '15-17', '15-17', '15-17', '15-17', '15-17', '15-17',
                '15-17', '15-17', '15-17', '15-17', '15-17', '15-17', '15-17', '15-17', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39',
                '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39',
                '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39', '18-39',
                '18-39', '18-39', '40-100', '40-100', '40-100', '15-17', '15-17', '15-17', '15-17', '15-17', '15-17', '15-17'],
        'Last Name': ['A-Z', 'A-Z', 'A-Z', 'A-Z', 'A-Z', 'A-G', 'H-Z', 'A-G', 'H-Z', 'A-Z', 'A-E', 'F-N', 'O-Z', 'A-M', 'N-Z', 'A-I', 'J-Z', 'A-G',
                      'H-M', 'N-Z', 'A-F', 'G-Z', '*TBA', 'A-J', 'K-Z', 'A-F', 'G-M', 'N-Z', 'A-J', 'K-Z', 'A-F', 'G-Z', 'A-M', 'N-Z', 'A-L', 'M-Z',
                      '*TBA', 'A-F', 'G-M', 'N-Z', 'A-E', 'F-Z', '*TBA', 'A-M', 'N-Z', 'A-E', 'F-N', 'O-Z', 'A-F', 'G-Z', '*TBA', 'A-M', 'N-Z', 'A-G',
                      'H-Z', 'A-G', 'H-Z', 'A-G', 'H-M', 'N-Z', 'A-F', 'G-Z', 'A-F', 'G-M', 'N-Z', 'A-J', 'K-Z', '*TBA', 'A-E', 'F-N', 'O-Z', 'A-M',
                      'N-Z', 'A-E', 'F-N', 'O-Z', 'A-F', 'G-Z', 'A-F', 'G-M', 'N-Z', 'A-F', 'G-M', 'N-Z', 'A-G', 'H-M', 'N-Z', 'A-I', 'J-Z', '*TBA',
                      'A-E', 'F-N', 'O-Z', 'A-E', 'F-N', 'O-Z', 'A-F', 'G-M', 'N-Z', 'A-F', 'G-M', 'N-Z', 'A-G', 'H-M', 'N-Z', 'A-I', 'J-Z', '*TBA',
                      'A-E', 'F-N', 'O-Z', 'A-E', 'F-N', 'O-Z', 'A-F', 'G-Z', 'A-F', 'G-M', 'N-Z', 'A-F', 'G-M', 'N-Z', 'A-G', 'H-M', 'N-Z', 'A-I',
                      'J-Z', '*TBA', 'A-F', 'G-M', 'N-Z', 'A-E', 'F-N', 'O-Z', 'A-F', 'G-M', 'N-Z', 'A-G', 'H-M', 'N-Z', 'A-E', 'F-N', 'O-Z', 'A-F',
                      'G-M', 'N-Z', '*TBA', 'A-E', 'F-N', 'O-Z', 'A-E', 'F-N', 'O-Z', 'A-F', 'G-Z', 'A-E', 'F-N', 'O-Z'],
        'Ring #': ['1', '2', '4', '6', '7', '8', '10', '11', '12', '13', '14', '15', '16', '17', '3', '9', '18', '5', '19', '20', '21', '22', '*TBA',
                   '10', '11', '12', '13', '14', '15', '16', '17', '3', '9', '18', '1', '2', '*TBA', '4', '5', '6', '7', '8', '*TBA', '10', '11',
                   '12', '13', '14', '15', '16', '*TBA', '17', '18', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                   '*TBA', '1', '2', '3', '4', '5', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                   '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '1', '2', '3',
                   '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '1', '2', '3', '4', '5', '6',
                   '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '1', '2', '3', '4', '5', '6', '7'],
        '# Comp': [4, 12, 10, 6, 0, 11, 10, 13, 13, 11, 2, 0, 7, 5, 8, 12, 0, 3, 7, 6, 9, 6, 0, 2, 5, 10, 9, 9, 2, 9, 9, 13, 12, 14, 12, 11, 0, 11,
                   10, 4, 0, 6, 5, 3, 6, 0, 3, 15, 11, 9, 14, 10, 12, 12, 4, 0, 1, 7, 8, 6, 7, 7, 13, 13, 2, 2, 7, 6, 12, 12, 15, 1, 0, 2, 5, 5, 13,
                   2, 0, 3, 4, 8, 7, 8, 8, 6, 14, 5, 5, 9, 6, 3, 5, 13, 11, 9, 5, 3, 6, 7, 12, 11, 8, 7, 5, 12, 3, 1, 6, 2, 2, 3, 9, 9, 10, 10, 11,
                   12, 7, 3, 4, 10, 10, 2, 2, 2, 8, 2, 4, 5, 4, 5, 14, 13, 13, 14, 5, 3, 3, 5, 3, 5, 2, 2, 5, 7, 7, 11, 10, 7, 6, 14, 8, 4, 12, 10, 2,
                   9, 13],
        'Center': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        'Corner': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    }

    envelope_df = pd.DataFrame(_normalize_sample_envelope_data(envelope_data))

    for col in ['Event_Time', 'Division', 'Rank', 'Age', 'Last Name', 'Ring #', 'Center', 'Corner']:
        envelope_df[col] = envelope_df[col].astype('string')

    TSR_pdf.add_summary_info_to_page(envelope_df)
    TSR_pdf.write_pdfpage()

if __name__ == "__main__":
    main()
