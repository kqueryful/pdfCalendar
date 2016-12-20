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
SIZE = pagesizes.portrait(pagesizes.letter)


class NoCanvasError(Exception):
    pass


def nonzero(row):
    return len([x for x in row if x!=0])


def createCalendar(month, year=NOW.year, canvas=None, filename=None, size=SIZE):
    """
    Create a one-month pdf calendar, add lines for every day, and return the canvas

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
    midSpace = height/2
    height = midSpace

    # draw the month title
    canvas.setFont('Helvetica-Bold', 22)
    title = monthName + ' ' + str(year)
    canvas.drawCentredString(width / 2, height - 35 + midSpace, title)
    height -= 50

    # margins
    wmar, hmar = width/35, width/35

    # set up constants
    width, height = width - (2*wmar), height - (2*hmar)
    rows, cols = len(cal), 7
    lastweek = nonzero(cal[-1])
    firstweek = nonzero(cal[0])
    rowheight = floor(height / rows)
    boxwidth = floor(width/7)

    # draw the bottom line
    canvas.line(wmar, hmar + midSpace, wmar+(boxwidth*lastweek), hmar + midSpace)
    # for all complete rows, draw the bottom line
    for row in range(1, len(cal[1:-1]) + 1):
        y = hmar + (row * rowheight) + midSpace
        canvas.line(wmar, y, wmar + (boxwidth * 7), y)
    # draw the top line of the first full row
    y = hmar + ((rows-1) * rowheight) + midSpace
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
        starty = hmar + (last * rowheight) + midSpace
        endy = hmar + (rows * rowheight) - (first * rowheight) + midSpace
        canvas.line(x, starty, x, endy)

    # weekday header
    canvas.setFont('Helvetica', 12)
    x = wmar + boxwidth/2
    y = hmar + (rows * rowheight) + 5 + midSpace
    for day in weekHeader:
        canvas.drawCentredString(x, y, day)
        x += boxwidth

    # fill in the day numbers
    x = wmar + 6
    y = hmar + (rows * rowheight) - 15 + midSpace
    for week in cal:
        for day in week:
            if day:
                canvas.drawString(x, y, str(day))
            x += boxwidth
        y -= rowheight
        x = wmar + 6

    # for each day in the month, provide some notes lines
    row = 12
    lastDay = max(cal[-1:][0])
    y = hmar + lastDay*row
    canvas.setFont('Helvetica',9)

    for day in range(1, lastDay + 1):
        canvas.drawString(wmar + 6, y+2, "{}".format(day))
        canvas.line(wmar, y, endx, y)
        y -= row


    # finish this page
    canvas.showPage()

    return canvas

if __name__ == "__main__":
    c = createCalendar(NOW.month, NOW.year, filename="calendar.pdf")
    # createCalendar(1, 2017, canvas=c)
    c.save()