import math
from scipy.integrate import quad

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

def integrand(a, b):
    return -1 * (a + b)

#variables for forecasting
windSpeedFuture1 = 0
temperatureFuture1 = 0

#variables from api
time1 = 946702800 #in seconds since Jan 1 1970
time2 = 946789200 #in seconds since Jan 1 1970

latitude1 = 25.761681 #in degrees
longitude1 = -80.191788 #in degrees
windSpeed1 = 1.33 #in miles per hour
windBearing1 = 73 #in degrees with true north at 0
temperature1 = 64.84 #in farenheit
pressure1 = 1021.7 #in millibars

latitude2 = 25.8103146 #in degrees
longitude2 = -80.1751609 #in degrees
windSpeed2 = 1.65 #in miles per hour
windBearing2 = 83 #in degrees with true north at 0
temperature2 = 65.29 #in farenheit
pressure2 = 1021.7 #in millibars

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
# omega = quad(integrand(dudx, dvdy), pressure1, pressure2)
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
temperatureFuture1 = (tempForecasted * 9 / 5) - 459.67

#results
print(windSpeedFuture1, temperatureFuture1)
#error = abs(experimental - actual)/actual * 100
