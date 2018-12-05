"""
   Convex Hull Assignment: COSC262 (2018)
   Student Name: Patrick Laffey
   Usercode: pla55
"""

from tkinter import *
from tkinter.ttk import *
import math
import timeit

def readDataPts(filename, N):
    """Reads the first N lines of data from the input file
          and returns a list of N tuples
          [(x0,y0), (x1, y1), ...]
    """
    file = open(filename)
    lines = []
    for i in range(0, N):
        line = file.readline().strip("\n")
        coords = line.split(" ")
        lines.append((float(coords[0]),float(coords[1])))
    return lines


def giftwrap(listPts):
    """Returns the convex hull vertices computed using the
          giftwrap algorithm as a list of m tuples
          [(u0,v0), (u1,v1), ...]    
    """
    path = []
    lowestPoint = getMinYPointIndex(listPts)
    firstNode = listPts[lowestPoint]
    path.append(firstNode)
    previousAngle = 0
    node, previousAngle = nextNode(firstNode, listPts, previousAngle)
    while node != firstNode and node != None:
        path.append(node)
        node, previousAngle = nextNode(node, listPts, previousAngle)
    return path

def nextNode(node, points, previousAngle):
    minAngle = 361
    nextPoint = None
    for point in points:
        angle = calcAngle(node, point)
        if angle < minAngle and angle > previousAngle and point != node:
            minAngle = angle
            nextPoint = point
    return nextPoint, minAngle

def getMinYPointIndex(listPts):
    minIndex = len(listPts) - 1
    indexCount = len(listPts) - 1
    while indexCount >= 0:
        if listPts[indexCount][1] < listPts[minIndex][1]:
            minIndex = indexCount
        elif listPts[indexCount][1] == listPts[minIndex][1]:
            if listPts[indexCount][0] > listPts[minIndex][0]:
                minIndex = indexCount
        indexCount -= 1
    return minIndex

def calcAngle(point1, point2):
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    angle = math.degrees(math.atan2(delta_y, delta_x))
    if angle < 0:
        return 360 + angle
    return angle

def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
         Graham-scan algorithm as a list of m tuples
         [(u0,v0), (u1,v1), ...]  
    """
    lowestPoint = listPts[getMinYPointIndex(listPts)]
    sortedPts = sortByAngle(lowestPoint, listPts)
    stack = [sortedPts.pop()]
    while len(sortedPts) > 0:
        node = sortedPts.pop()
        lineStart = stack[len(stack) - 1]
        lineEnd = stack[len(stack) - 2]
        stack.append(node)
        while not isLeftOfLine(lineStart, lineEnd, node) and len(stack) > 3:
           stack.pop(len(stack) - 2)
    return stack

def isLeftOfLine(lineStart, lineEnd, point):
    y = (point[0] - lineStart[0]) * (lineEnd[1] - lineStart[1])
    x = (point[1] - lineStart[1]) * (lineEnd[0] - lineStart[1])
    if (x - y) > 0:
        return False
    return True

def sortByAngle(anchor, points):
    angles = {}
    for point in points:
        angles[point] = calcAngle(anchor, point)
    return sorted(angles, key=angles.__getitem__, reverse=True)

def amethod(listPts):
    """Returns the convex hull vertices computed using 
          a third algorithm (Monotone Chain)
    """
    leftSortedPts = sorted(listPts)
    upper = []
    lower = []
    for point in leftSortedPts:
        while len(lower) >= 2 and crossProduct(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(leftSortedPts):
        while len(upper) >= 2 and crossProduct(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    upper.pop()
    lower.pop()
    return upper + lower

def crossProduct(pt1, pt2, pt3):
    return (pt2[0] - pt1[0]) * (pt3[1] - pt1[1]) - (pt2[1] - pt1[1]) * (pt3[0] - pt1[0])

def validate(edge, allPoints, header):
    print(header +" Results:")
    print(edge)
    master = Tk()
    master.title(header)
    canvas = Canvas(master, height = 500, width = 500, bg = "beige")
    canvas.pack()
    for point in allPoints:
        addPoint(canvas, point)
    canvas.update()
    count = 0
    while count < len(edge) - 1:
        addLine(canvas, edge[count], edge[count + 1])
        canvas.update()
        count += 1
    addLine(canvas, edge[count], edge[0])
    print("Completed " + header + "\n")

def addPoint(canvas, point):
    canvas.create_oval(point[0]/2, point[1]/2, point[0]/2, point[1]/2, fill="red", outline="red", width=1)

def addLine(canvas, points1, points2):
    canvas.create_line(points1[0]/2, points1[1]/2, points2[0]/2, points2[1]/2)

def timeMethod(listPts, method):
    SETUP = "from __main__ import " + method
    CODE = "listPts = " + str(listPts) + "\n" + method + "(listPts)"
    return min(timeit.repeat(stmt = CODE, setup = SETUP, number = 1, repeat = 5))
              
def main():
    datafile = ["A_", "B_"]
    print("Filename    | Gift Wrap Time | Graham Scan Time | Monotone Chain Time")
    for file in datafile:
        points = 3000
        count = 1
        while count <= 10:
            filename = file + str(count * points) + ".dat"
            listPts = readDataPts("datafiles/" + filename, count * points)  #File name, numPts given as example only
            print(filename + (" " * abs(12 - len(filename))) + "|", end=' ')
            print("%.10Fs  |" % timeMethod(listPts, "giftwrap"), end = ' ')
            print("%.10Fs    |" % timeMethod(listPts, "grahamscan"), end = ' ')
            print("%.10Fs" % timeMethod(listPts, "amethod"))
            count += 1
            
if __name__  ==  "__main__":
    main()
