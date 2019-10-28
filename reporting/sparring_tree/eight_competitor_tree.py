""" this module contains code to create an 8 person sparring tree"""


from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm

from reportlab.pdfgen import canvas


class EightCompetitorTree():
    """ Creates an 8 compettitor sparring tree"""
    _c = None
    _path = None

    def __init__(self, canvas):
        """ sets up instance variables for this tree """
        self._c = canvas
        self._c.setPageSize(letter)  # defaults to 72 pointer per inch
        self._path = self._c.beginPath()
        # print(self._c.__dict__)
        print('EightCompetitorTree initialized with filename:' + self._c.__dict__['_filename'])

    def close(self):
        """ generate the page"""
        self._c.drawPath(self._path, stroke=1, fill=0)
        self._c.showPage()

    def draw_box(self, left, top):
        ''' draw a single checkbox at the coordinates provided '''
        self._path.moveTo(left * cm, top * cm)
        self._path.lineTo((left - .3) * cm, (top * cm))
        self._path.lineTo((left - .3) * cm, (top - .3) * cm)
        self._path.lineTo(left * cm, (top - .3) * cm)
        self._path.lineTo(left * cm, top * cm)

    def draw_boxes(self, left, top):
        ''' draw checkboxes at the coordinates provides to keep track of scores '''
        self.draw_box(left, top)
        self.draw_box(left + .8, top)
        self.draw_box(left + 1.6, top)

    def draw_static_template(self):
        """ Draws the static templatized portion of the tree"""
        # First bracket
        for i in range(4):
            offset = i * 4.8
            self._path.moveTo(.8 * cm, (3.8 + offset) * cm)  # 3/4 inch to the right, 1.5 inches up
            self._path.lineTo(6 * cm, (3.8 + offset) * cm)
            self._path.lineTo(7.2 * cm, (5 + offset) * cm)
            self._path.lineTo(6 * cm, (6 + offset) * cm)
            self._path.lineTo(.8 * cm, (6 + offset) * cm)
            self.draw_boxes(1.5, 5.3 + offset)  # 9/16 inches to the right and 2.125 inches up
            self.draw_boxes(1.5, 7.5 + offset)  # 9/16 inches to the right and 4 inches up

        # Second bracket
        for i in range(2):
            offset = i * 9.6
            self._path.moveTo(7.2 * cm, (5 + offset) * cm)  # 2.75 inch to the right, 2 inches up
            self._path.lineTo(12.4 * cm, (5 + offset) * cm)
            self._path.lineTo(15.2 * cm, (7.5 + offset) * cm)
            self._path.lineTo(12.4 * cm, (9.8 + offset) * cm)
            self._path.lineTo(7.2 * cm, (9.8 + offset) * cm)
            self.draw_boxes(7.5, 6.4 + offset)  # 9/16 inches to the right and 4 inches up
            self.draw_boxes(7.5, 11.3 + offset)  # 9/16 inches to the right and 4 inches up

        # third bracket
        self._path.moveTo(15.2 * cm, 7.5 * cm)  # 2.9375 inch to the right, 6 inches up
        self._path.lineTo(20.4 * cm, 7.5 * cm)
        self._path.moveTo(15.2 * cm, 17.1 * cm)
        self._path.lineTo(20.4 * cm, 17.1 * cm)

        self.draw_boxes(15.5, 9)  # 9/16 inches to the right and 4 inches up
        self.draw_boxes(15.5, 18.7)  # 9/16 inches to the right and 4 inches up


if __name__ == '__main__':
    ''' Very simple test try to create a tree and check that the file exists '''
    c = canvas.Canvas("8PersonTree.pdf", pagesize=letter)  # defaults to 72 pointer per inch
    tree = EightCompetitorTree(c)
    tree.draw_static_template()
    tree.close()
    c.save()
    import os

    if os.path.exists("8PersonTree.pdf"):
        print("It worked")
