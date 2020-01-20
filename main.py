from sklearn import tree
from sklearn.externals.six import StringIO
from IPython.display import Image
import pydotplus
import csv
import math

# declare vars
features = []
features_names = ['precipIntensity', 'precipProbability', 
            'temperature', 'apparentTemperature', 'dewPoint', 
            'humidity', 'pressure', 'windSpeed', 'windBearing', 
            'cloudCover', 'uvIndex', 'visibility']
label_names = []
labels = []
clf = None

def readDecisionTreeData(filename):
    #get data in csv
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                l = row[1]
                if l not in label_names:
                    label_names.append(l)
                labels.append(label_names.index(l))
                f = []
                for i in range(2,14):
                    f.append(row[i])
                features.append(f)
                line_count += 1

def makeDecisionTree():
    # make decision tree
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(features, labels)

def printDecisionTree():
    dot_data = StringIO()
    tree.export_graphviz(clf, 
                        out_file=dot_data,
                        feature_names=features_names,
                        class_names=label_names,
                        filled=True,
                        rounded=True,
                        impurity=False)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_pdf("weather_tree.pdf")

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

def calculateNWP(time1, latitude1, longitude1, windSpeed1, windBearing1, temperature1, pressure1, 
                    time2, latitude2, longitude2, windSpeed2, windBearing2, temperature2, pressure2):
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
    dudp = (u2 - u1) / (pressure2 - pressure1) if (pressure2 - pressure1) != 0.0 else 0.0
    dvdp = (v2 - v1) / (pressure2 - pressure1) if (pressure2 - pressure1) != 0.0 else 0.0
    dpdx = (pressure2 - pressure1) / (deltax)
    dpdy = (pressure2 - pressure1) / (deltay)
    dTdx = (temperature2 - temperature1) / (deltax)
    dTdy = (temperature2 - temperature1) / (deltay)
    dTdp = (temperature2 - temperature1) / (pressure2 - pressure1) if (pressure2 - pressure1) != 0.0 else 0.0

    dudt = (-1 * u1 * dudx) - (v1 * dudy) - (dudp) + (f1 * v1) - ((1/density1) * dpdx)
    dvdt = (-1 * u1 * dvdx) - (v1 * dvdy) - (dvdp) + (f1 * u1) - ((1/density1) * dpdy)
    dTdt = (-1 * u1 * dTdx) - (v1 * dTdy) - (dTdp - ((R * temperature1) / (cp * pressure1))) #cp is missing

    uForecasted = u1 + (dudt * (time2 - time1))
    vForecasted = v1 + (dvdt * (time2 - time1))
    tempForecasted = temperature1 + (dTdt * (time2 - time1))

    #convert back
    uForecasted = uForecasted / 0.00062137 #metres per second to miles per second
    vForecasted = vForecasted / 0.00062137 #metres per second to miles per second
    windSpeedFuture1 = (math.sqrt(math.pow(uForecasted, 2) + math.pow(vForecasted, 2))) * 3600
    temperatureFuture1 = (tempForecasted * 9 / 5) - 459.67

    #results
    return windSpeedFuture1, temperatureFuture1
