#!/usr/bin/env python
"""Create a PDF calendar.

Requires Reportlab
( http://reportlab.org/rl_toolkit.html )
"""
from reportlab.lib import pagesizes
from reportlab.pdfgen.canvas import Canvas
import calendar, time, datetime
from math import floor

NOW = datetime.datetime.now()
SIZE = pagesizes.landscape(pagesizes.letter)


class NoCanvasError(Exception):
    pass


def nonzero(row):
    return len([x for x in row if x!=0])


def createCalendar(month, year=NOW.year, canvas=None, filename=None, size=SIZE):
    """
    Create a one-month pdf calendar, and return the canvas

    month: an integer (1=Jan, 12=Dec)
    year: year in which month falls. Defaults to current year.
    canvas: you may pass in a canvas to add a calendar page to the end.
    filename: String containing the file to write the calendar to
    size: size, in points of the canvas to write on
    """

    if canvas is None and filename is not None:
        canvas = Canvas(filename, size)
    elif canvas is None and filename is None:
        raise NoCanvasError

    monthName = time.strftime("%B", time.strptime(str(month), "%m"))
    weekHeader = calendar.weekheader(3).split()
    cal = calendar.monthcalendar(year, month)

    width, height = size

    # draw the month title
    title = monthName + ' ' + str(year)
    canvas.drawCentredString(width / 2, height - 35, title)
    height -= 50

    # margins
    wmar, hmar = width/35, height/35

    # set up constants
    width, height = width - (2*wmar), height - (2*hmar)
    rows, cols = len(cal), 7
    lastweek = nonzero(cal[-1])
    firstweek = nonzero(cal[0])
    rowheight = floor(height / rows)
    boxwidth = floor(width/7)

    # draw the bottom line
    canvas.line(wmar, hmar, wmar+(boxwidth*lastweek), hmar)
    # for all complete rows, draw the bottom line
    for row in range(1, len(cal[1:-1]) + 1):
        y = hmar + (row * rowheight)
        canvas.line(wmar, y, wmar + (boxwidth * 7), y)
    # draw the top line of the first full row
    y = hmar + ((rows-1) * rowheight)
    canvas.line(wmar, y, wmar + (boxwidth * 7), y)
    # draw the top line of the first row
    startx = wmar + (boxwidth * (7-firstweek))
    endx = startx + (boxwidth * firstweek)
    y += rowheight
    canvas.line(startx, y, endx, y)

    # draw the vertical lines
    for col in range(8):
        #1 = don't draw line to first or last; 0 = do draw
        last, first = 1, 1
        if col <= lastweek: last = 0
        if col >= 7 - firstweek: first = 0
        x = wmar + (col * boxwidth)
        starty = hmar + (last * rowheight)
        endy = hmar + (rows * rowheight) - (first * rowheight)
        canvas.line(x, starty, x, endy)

    # weekday header
    x = wmar + boxwidth/2
    y = hmar + (rows * rowheight) + 5
    for day in weekHeader:
        canvas.drawCentredString(x, y, day)
        x += boxwidth

    # fill in the day numbers
    x = wmar + 6
    y = hmar + (rows * rowheight) - 15
    for week in cal:
        for day in week:
            if day:
                canvas.drawString(x, y, str(day))
            x += boxwidth
        y -= rowheight
        x = wmar + 6

    # finish this page
    canvas.showPage()

    return canvas

if __name__ == "__main__":
    c = createCalendar(NOW.month, NOW.year, filename="calendar.pdf")
    # createCalendar(1, 2017, canvas=c)
    c.save()