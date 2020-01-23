import csv
import numpy

def readFromFile(filename, timestamp, days):
    arr = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rec = False
        i = 0
        line = 0
        for row in csv_reader:
            if line != 0:
                a = []
                for j in range(2, len(row)):
                    a.append(float(row[j]))
            if row[0] == str(timestamp):
                i = 0
                rec = True
            if rec and i < days:
                arr.append(a)
                i = i + 1
            if i == days:
                return arr
            line = line + 1

def makeSlidingWindow(arr, windowLength):
    arr2 = []
    i = 0
    j = 0
    while i + j < len(arr):
        tmpArr = []
        for j in range(windowLength):
            tmpArr.append(arr[i + j])
        arr2.append(tmpArr)
        i = i + 1
    return arr2

def calcEuclideanDist(arr2d1, arr2d2):
    a = numpy.array(arr2d1)
    b = numpy.array(arr2d2)
    return numpy.linalg.norm(a)

CD = readFromFile('weather_data_miami.csv', 1514696400, 7) #current data from January 1 2018
PD = readFromFile('weather_data_miami.csv',1483160400,14) #past data from January 1 2017
W = makeSlidingWindow(PD, 7)
ED = []
for i in range(len(W)):
    ED.append(calcEuclideanDist(W[i], CD))
Wi = W[ED.index(min(ED))]

# a = [1, 2, 3, 4, 5, 6]
# b = [4, 5, 6, 7, 8, 9]
# c = [[-4, -3, -2], [-1,  0,  1], [ 2,  3,  4]]
# d = [-4, -3, -2, -1, 0, 1,  2,  3,  4]
# e = numpy.array((1, 2, 3, 4, 5, 6))
# f = numpy.array((4, 5, 6, 7, 8, 9))
# h = numpy.array([[ 1, 2, 3], [4, 5, 6]])
# i = numpy.array([[ 4, 5, 6], [7, 8, 9]])
# g = f - e
# print(numpy.linalg.norm(a))
# print(numpy.linalg.norm(b))
# print(numpy.linalg.norm(c))
# print(numpy.linalg.norm(d))
# print(numpy.linalg.norm(f-e))
# print(numpy.linalg.norm(g))
# print(numpy.linalg.norm(i-h))
