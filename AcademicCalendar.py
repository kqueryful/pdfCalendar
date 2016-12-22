#!/usr/bin/env python
"""Create a PDF calendar.

Requires Reportlab
( http://reportlab.org/rl_toolkit.html )
"""
import arrow
import calendar
from reportlab.lib import pagesizes, colors
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen.canvas import Canvas


SIZE = pagesizes.portrait(pagesizes.letter)
NUMWEEKS = 10


class mo:
    def __init__(self, name, cal):
        self.name = name
        self.cal = cal


def createCalendar(start, end, filename=None, size=SIZE, color=colors.red):
    """
    Create an academic calendar for a quarter.
    Counts academic weeks + 1 week for finals.

    start: an Arrow date
    end: an Arrow date
    filename: String containing the file to write the calendar to
    size: size, in points of the canvas to write on
    color: color for accents
    """

    # initializations
    canvas = Canvas(filename, size)
    weekHeader = calendar.weekheader(1).split()
    weekHeader.insert(0, 0)
    width, height = size

    # dictionary for each month in quarter
    months = 1
    monthInfo = {}

    for dt in arrow.Arrow.range('month', start.replace(day=1), end.replace(day=2)):
        name = dt.format('MMM')
        cal = calendar.monthcalendar(dt.year, dt.month)
        monthInfo[months] = mo(name, cal)
        months += 1

    # arrange array for printing
    fullCal = []
    fullCal.append(weekHeader)
    weekNum = 1

    for m in monthInfo:
        weekNum -= 1
        fullCal.append(monthInfo[m].name)
        for w in monthInfo[m].cal:
            # add academic week numbers
            if (m == 1 and max(w) >= start.day) or weekNum > 0:
                weekNum += 1
            if weekNum > NUMWEEKS + 1:
                weekNum = 0

            w.insert(0, weekNum)
            fullCal.append(w)

    # draw everything out
    cellWidth = .3 * inch
    cellHeight = .3 * inch
    x = 1.5 * inch
    y = height - inch
    canvas.setStrokeAlpha(.25)

    for week in fullCal:
        # found a month
        if type(week) is str:
            canvas.setFont('Helvetica-Bold', 11)
            canvas.setFillColor(color)
            canvas.drawString(inch, y, week)
            canvas.setFillColor(colors.black)
            canvas.setFont('Helvetica', 11)
        else:  # found an array for weekdays
            for d, day in enumerate(week):
                if day != 0:
                    # weekday abbreviations
                    if type(day) is str:
                        canvas.setFont('Helvetica-Bold', 11)
                    else:
                        canvas.setFont('Helvetica', 11)

                    # draw circles around all the week numbers
                    if d == 0:
                        canvas.circle(x, y + .05 * inch, .1 * inch)

                    # weekends
                    if d in (6,7):
                        canvas.setFillColor(color)
                    else:
                        canvas.setFillColor(colors.black)

                    canvas.drawCentredString(x, y, str(day))
                x += cellWidth
            x = 1.5 * inch
            y -= cellHeight

    # finish this page
    canvas.showPage()
    return canvas

if __name__ == "__main__":
    # PDF for winter 2017
    c = createCalendar(arrow.get(2017, 1, 9), arrow.get(2017, 3, 25), filename="quarter.pdf", color=colors.red)
    c.save()