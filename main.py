import time
import sys
from sklearn import tree
from sklearn.externals.six import StringIO
from sklearn.externals import joblib
from IPython.display import Image
import pydotplus
import csv
import math
import numpy
import queue
from multiprocessing import Process, Pipe
from threading import Thread

# declare vars
weatherParams = ['precipIntensity', 'precipProbability', 'temperature', 'humidity', 'pressure', 'windSpeed', 'windBearing']

def saveTree(filename, clf):
    joblib.dump(clf, filename)

def loadTree(filename):
    return joblib.load(filename)

def printDecisionTree(clf, outputfile, features_names, label_names):
    dot_data = StringIO()
    tree.export_graphviz(clf, 
                        out_file=dot_data,
                        feature_names=features_names,
                        class_names=label_names,
                        filled=True,
                        rounded=True,
                        impurity=False)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_pdf(outputfile)

def calculateDistance(lat1, long1, lat2, long2):#haversine formula
    r = 6371 * pow(10, 3)
    theta1 = math.radians(lat1)
    theta2 = math.radians(lat2)
    deltaTheta = math.radians(lat2 - lat1)
    deltaLambda = math.radians(long2 - long1)
    a = (math.sin(deltaTheta/2) * math.sin(deltaTheta/2)) + (math.cos(theta1) * math.cos(theta2) * math.sin(deltaLambda/2) * math.sin(deltaLambda/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = r * c
    y = math.sin(deltaLambda) * math.cos(theta2)
    x = (math.cos(theta1) * math.sin(theta2)) - (math.sin(theta1) * math.cos(theta2) * math.cos(deltaLambda))
    bearing = (math.atan2(y, x) + math.pi) % math.pi
    return distance, bearing

def calculateNWP(time1, time2, 
                    latitude1, longitude1, windSpeed1, windBearing1, temperature1, pressure1, 
                    latitude2, longitude2, windSpeed2, windBearing2, temperature2, pressure2):
    #variables for forecasting
    windSpeedFuture1 = 0
    temperatureFuture1 = 0
    
    #constants
    g = 9.79433 #in meters per second square
    Rdry = 0.287058 #in joules per (gram Kelvin)
    R = 8.314 #in joules per (Kelvin mol)
    omg = 7.27 * pow(10, -5) #in rad per seconds
    cp = 1.01 #in joules per (gram Kelvin)

    #conversions
    windBearing1 = math.radians(windBearing1) #degrees to radians
    windBearing2 = math.radians(windBearing2) #degrees to radians
    windSpeed1 = windSpeed1 * 0.00062137 / 3600 #miles per hour to metres per second
    windSpeed2 = windSpeed2 * 0.00062137 / 3600 #miles per hour to metres per second
    temperature1 = (temperature1 + 459.67) * 5/9 #farenheit to Kelvin
    temperature2 = (temperature2 + 459.67) * 5/9 #farenheit to Kelvin
    pressure1 = pressure1 * 100 #millibars to pascals
    pressure2 = pressure2 * 100 #millibars to pascals

    #calculations
    density1 = pressure1 / (Rdry * temperature1)
    f1 = 2 * omg * math.sin(math.radians(latitude1))
    distance, angle = calculateDistance(latitude1, longitude1, latitude2, longitude2)
    deltax = distance * math.cos(angle)
    deltay = distance * math.sin(angle)

    u1 = 0
    v1 = 0
    u2 = 0
    v2 = 0
    if windBearing1 == 0:
        u1 = 0
        v1 = windSpeed1
    elif windBearing1 == 90:
        u1 = -windSpeed1
        v1 = 0
    elif windBearing1 == 180:
        u1 = 0
        v1 = -windSpeed1
    elif windBearing1 == 270:
        u1 = windSpeed1
        v1 = 0
    elif windBearing1 > 0 and windBearing1 < 90:
        u1 = -windSpeed1 * math.sin(windBearing1)
        v1 = windSpeed1 * math.cos(windBearing1)
    elif windBearing1 > 90 and windBearing1 < 180: 
        u1 = -windSpeed1 * math.cos(windBearing1 - 90)
        v1 = -windSpeed1 * math.sin(windBearing1 - 90)
    elif windBearing1 > 180 and windBearing1 < 270: 
        u1 = windSpeed1 * math.sin(windBearing1 - 180)
        v1 = windSpeed1 * math.cos(windBearing1 - 180)
    else:
        u1 = windSpeed1 * math.cos(windBearing1 - 270)
        v1 = windSpeed1 * math.sin(windBearing1 - 270)
    if windBearing2 == 0:
        u2 = 0
        v2 = windSpeed2
    elif windBearing2 == 90:
        u2 = -windSpeed2
        v2 = 0
    elif windBearing2 == 180:
        u2 = 0
        v2 = -windSpeed2
    elif windBearing2 == 270:
        u2 = windSpeed2
        v2 = 0
    elif windBearing2 > 0 and windBearing2 < 90:
        u2 = -windSpeed2 * math.sin(windBearing2)
        v2 = windSpeed2 * math.cos(windBearing2)
    elif windBearing2 > 90 and windBearing2 < 180: 
        u2 = -windSpeed2 * math.cos(windBearing2 - 90)
        v2 = -windSpeed2 * math.sin(windBearing2 - 90)
    elif windBearing2 > 180 and windBearing2 < 270: 
        u2 = windSpeed2 * math.sin(windBearing2 - 180)
        v2 = windSpeed2 * math.cos(windBearing2 - 180)
    else:
        u2 = windSpeed2 * math.cos(windBearing2 - 270)
        v2 = windSpeed2 * math.sin(windBearing2 - 270)

    dudx = (u2 - u1) / (deltax)
    dvdx = (v2 - v1) / (deltax)
    dudy = (u2 - u1) / (deltay)
    dvdy = (v2 - v1) / (deltay)
    omega = (pressure2 - pressure1) * -1 * (dudx + dvdy)
    dudp = (u2 - u1) / (pressure2 - pressure1) if (pressure2 - pressure1) != 0.0 else 0.0
    dvdp = (v2 - v1) / (pressure2 - pressure1) if (pressure2 - pressure1) != 0.0 else 0.0
    dpdx = (pressure2 - pressure1) / (deltax)
    dpdy = (pressure2 - pressure1) / (deltay)
    dTdx = (temperature2 - temperature1) / (deltax)
    dTdy = (temperature2 - temperature1) / (deltay)
    dTdp = (temperature2 - temperature1) / (pressure2 - pressure1) if (pressure2 - pressure1) != 0.0 else 0.0

    dudt = (-1 * u1 * dudx) - (v1 * dudy) - (omega * dudp) + (f1 * v1) - ((1/density1) * dpdx)
    dvdt = (-1 * u1 * dvdx) - (v1 * dvdy) - (omega * dvdp) + (f1 * u1) - ((1/density1) * dpdy)
    dTdt = (-1 * u1 * dTdx) - (v1 * dTdy) - (omega * (dTdp - ((R * temperature1) / (cp * pressure1))))

    uForecasted = u1 + (dudt * (time2 - time1))
    vForecasted = v1 + (dvdt * (time2 - time1))
    tempForecasted = temperature1 + (dTdt * (time2 - time1))

    #convert back
    uForecasted = uForecasted / 0.00062137 #metres per second to miles per second
    vForecasted = vForecasted / 0.00062137 #metres per second to miles per second
    windSpeedFuture1 = (math.sqrt(math.pow(uForecasted, 2) + math.pow(vForecasted, 2))) * 3600
    windBearingFuture1 = math.degrees(math.atan(abs(vForecasted)/abs(uForecasted)))
    temperatureFuture1 = (tempForecasted * 9 / 5) - 459.67

    #results
    return temperatureFuture1, windSpeedFuture1, windBearingFuture1

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

def calcMean(arr):
    sum = 0
    for i in range(len(arr)):
        sum = sum + arr[i]
    return sum / len(arr)

def slidingWindowWeather(CD, PD, days):
    W = makeSlidingWindow(PD, days)
    ED = []
    for i in range(len(W)):
        ED.append(calcEuclideanDist(W[i], CD))
    Wi = W[ED.index(min(ED))]
    predicted = CD[len(CD) - 1]
    for i in range(len(CD[0])):
        variationCDVector = []
        variationPDVector = []
        for j in range(1, len(CD)):
            variationCDVector.append(CD[j][i] - CD[j - 1][i])
        for j in range(1, len(Wi)):
            variationPDVector.append(Wi[j][i] - Wi[j - 1][i])
        m1 = calcMean(variationCDVector)
        m2 = calcMean(variationPDVector)
        V = (m1 + m2) / 2
        predicted[i] = predicted[i] + V
    return predicted

def getTimeData(subQueue, filename):
    times = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line = 0
        for row in csv_reader:
            if line != 0: times.append(int(row[0]))
            line = line + 1
    subQueue.put(times)

def getForecastData(subQueue, filename):
    forecasts = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line = 0
        for row in csv_reader:
            if line != 0: forecasts.append(row[1])
            line = line + 1
    subQueue.put(forecasts)

def getWeatherData(subQueue, filename, wtParams):
    weatherData = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line = 0
        paramIndices = []
        for row in csv_reader:
            if line == 0:
                for i in range(len(wtParams)):
                    if wtParams[i] in row:
                        paramIndices.append(row.index(wtParams[i]))
            else:
                tmp = []
                for i in paramIndices:
                    tmp.append(float(row[i]))
                weatherData.append(tmp)
            line = line + 1
    subQueue.put(weatherData)

def getData(mainQueue, filename, wtParams):
    subQueue = queue.Queue()
    t1 = Thread(getTimeData(subQueue, filename))
    t2 = Thread(getForecastData(subQueue, filename))
    t3 = Thread(getWeatherData(subQueue, filename, wtParams))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    mainQueue.put([subQueue.get(), subQueue.get(), subQueue.get()])

def mlTrain(mainQueue, weatherDataLoc, forecasts):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(weatherDataLoc, forecasts)
    mainQueue.put(clf)

def nwpModel(mainQueue, currentDate, lat1, long1, lat2, long2, wD1L1, wD2L1, wD3L1, wD4L1, wD1L2, wD2L2, wD3L2, wD4L2):
    nwpCalcLoc = calculateNWP(
                currentDate, currentDate+(24 * 3600), 
                lat1, long1, wD1L1, wD2L1, wD3L1, wD4L1,
                lat2, long2, wD1L2, wD2L2, wD3L2, wD4L2)
    mainQueue.put(nwpCalcLoc)

def slidingWindowModel(mainQueue, currentDate, times, weatherDataLoc):
    CD = []
    PD = []
    nwpStartDate1 = currentDate - 518400
    if nwpStartDate1 in times:
        timesIndex1 = times.index(nwpStartDate1)
        for i in range(timesIndex1, timesIndex1 + 7):
            CD.append(weatherDataLoc[i])
    nwpStartDate2 = currentDate - 1123200
    if nwpStartDate2 in times:
        timesIndex2 = times.index(nwpStartDate2)
        for i in range(timesIndex2, timesIndex2 + 14):
            PD.append(weatherDataLoc[i])
    slidingWindowPrediction =  slidingWindowWeather(CD, PD, 7)
    mainQueue.put(slidingWindowPrediction)

if __name__ == '__main__':
    beginProgram = time.time()
    predictions = []
    q = queue.Queue()
    t1 = Thread(getData(q, './input/weather_data_miami.csv', weatherParams.copy()))
    t2 = Thread(getData(q, './input/weather_data_miami_beach.csv', weatherParams.copy()))
    t3 = Thread(getData(q, './input/weather_data_miami_hollywood.csv', weatherParams.copy()))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    d1 = q.get()
    times = d1[0]
    forecasts = d1[1]
    weatherDataLoc1 = d1[2]
    weatherDataLoc2 = q.get()[2]
    weatherDataLoc3 = q.get()[2]
    startDate = 1514696400 #January 1 2018
    endDate = 1515301200 #January 7 2018
    #run models
    q = queue.Queue()
    t0 = Thread(mlTrain(q, weatherDataLoc1, forecasts))
    t0.start()
    #run for 7 days
    currentDate = startDate
    dateIndex = times.index(currentDate)
    t1 = Thread(nwpModel(q, currentDate, 
                    25.761681, -80.191788, 
                    25.8103146, -80.1751609,
                    weatherDataLoc1[dateIndex][5], 
                    weatherDataLoc1[dateIndex][6], 
                    weatherDataLoc1[dateIndex][2], 
                    weatherDataLoc1[dateIndex][4],
                    weatherDataLoc2[dateIndex][5], 
                    weatherDataLoc2[dateIndex][6], 
                    weatherDataLoc2[dateIndex][2], 
                    weatherDataLoc2[dateIndex][4]))
    t2 = Thread(nwpModel(q, currentDate, 
                    25.761681, -80.191788, 
                    25.8103146, -80.1751609,
                    weatherDataLoc1[dateIndex][5], 
                    weatherDataLoc1[dateIndex][6], 
                    weatherDataLoc1[dateIndex][2], 
                    weatherDataLoc1[dateIndex][4],
                    weatherDataLoc2[dateIndex][5], 
                    weatherDataLoc2[dateIndex][6], 
                    weatherDataLoc2[dateIndex][2], 
                    weatherDataLoc2[dateIndex][4]))
    t3 = Thread(slidingWindowModel(q, currentDate, times, weatherDataLoc1))
    t1.start()
    t2.start()
    t3.start()
    t0.join()
    t1.join()
    t2.join()
    t3.join()
    machineLearning = q.get()
    nwp1 = q.get()
    nwp2 = q.get()
    sw = q.get()
    #nwp2+nwp1
    predictedForecast = machineLearning.predict([sw])
    predictions.append([str(currentDate) + ', ' + predictedForecast[0] + ',' + ', '.join(map(str, sw))])
    currentDate = currentDate + (24 * 3600)
    while currentDate < endDate:
        dateIndex = times.index(currentDate)
        t1 = Thread(nwpModel(q, currentDate, 
                        25.761681, -80.191788, 
                        25.8103146, -80.1751609,
                        weatherDataLoc1[dateIndex][5], 
                        weatherDataLoc1[dateIndex][6], 
                        weatherDataLoc1[dateIndex][2], 
                        weatherDataLoc1[dateIndex][4],
                        weatherDataLoc2[dateIndex][5], 
                        weatherDataLoc2[dateIndex][6], 
                        weatherDataLoc2[dateIndex][2], 
                        weatherDataLoc2[dateIndex][4]))
        t2 = Thread(nwpModel(q, currentDate, 
                        25.761681, -80.191788, 
                        25.8103146, -80.1751609,
                        weatherDataLoc1[dateIndex][5], 
                        weatherDataLoc1[dateIndex][6], 
                        weatherDataLoc1[dateIndex][2], 
                        weatherDataLoc1[dateIndex][4],
                        weatherDataLoc2[dateIndex][5], 
                        weatherDataLoc2[dateIndex][6], 
                        weatherDataLoc2[dateIndex][2], 
                        weatherDataLoc2[dateIndex][4]))
        t3 = Thread(slidingWindowModel(q, currentDate, times, weatherDataLoc1))
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        nwp1 = q.get()
        nwp2 = q.get()
        sw = q.get()
        #nwp2+nwp1
        predictedForecast = machineLearning.predict([sw])
        predictions.append([str(currentDate) + ', ' + predictedForecast[0] + ',' + ', '.join(map(str, sw))])
        currentDate = currentDate + (24 * 3600)
    #calculate program time
    endProgram = time.time()
    print('Program in single takes: ' + str(endProgram-beginProgram) + ' seconds')
    for a in predictions:
        print(a)

