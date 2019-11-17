from datetime import datetime
import time
import requests
import csv

date = datetime(1999,12,31)
timestamp = int(datetime.timestamp(date)) #Keep adding 86400 to increment by day
timestampE = int(datetime.timestamp(datetime(2018,12,31)))
#print((timestampE-timestamp)/86400)
i = 1
j = 1
fields = ['time', 'summary', 'precipIntensity', 'precipProbability', 
            'temperature', 'apparentTemperature', 'dewPoint', 
            'humidity', 'pressure', 'windSpeed', 'windBearing', 
            'cloudCover', 'uvIndex', 'visibility', 'nearestStormDistance']
COST = 1000
complete = 25

with open('weather_data.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(fields)
csvFile.close()

while True:
    #Get data from website
    values = []
    req='https://api.darksky.net/forecast/b96bb9a5ac2fd6d4dbafafa064810821/25.761681,%20-80.191788,'+str(timestamp+(86400*(i)))
    response = requests.get(req)
    if response.status_code == 200:
        data = response.json()
        for d in fields:
            try:
                values.append(data['currently'][d])
            except:
                values.append(-1)
    #Dump data in csv file
    with open('weather_data.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(values)
    csvFile.close()
    #increment i & j
    i = i + 1
    j = j + 1
    #if j == 1000 then wait until next day
    if j == COST-complete:
        complete = 0
        time.sleep(86400)
    #if i == int((timestampE-timestamp)/86400) then break
    if i == int((timestampE-(timestamp+86400))/86400):
        break
