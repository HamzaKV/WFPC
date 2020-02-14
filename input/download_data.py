from datetime import datetime
import time
import requests
import csv

timestamp = int(datetime.timestamp(datetime(1999,12,31))) #Keep adding 86400 to increment by day
timestampE = int(datetime.timestamp(datetime(2018,12,31)))
i = 1
j = 1
fields = ['time', 'summary', 'precipIntensity', 'precipProbability', 
            'temperature', 'apparentTemperature', 'dewPoint', 
            'humidity', 'pressure', 'windSpeed', 'windBearing', 
            'cloudCover', 'uvIndex', 'visibility', 'nearestStormDistance']
COST = 995
APIKEY = ''
with open('api') as api_file:
    APIKEY = api_file.readline()
net_tries = 0
wait_icon = "|"

while True:
    print("Printing..."+wait_icon, end="\r", flush=True)
    if wait_icon == "|":
        wait_icon = "/"
    elif wait_icon == "/":
        wait_icon = "-"
    elif wait_icon == "-":
        wait_icon = "\\"
    else:
        wait_icon="|"
    #Get data from website
    values = []
    #Locations: Miami,FL:25.761681,-80.191788 | Miami Beach,FL: 25.8103146,-80.1751609 | N Park Rd,Hollywood,FL: 26.0331192,-80.1774954
    req='https://api.darksky.net/forecast/'+APIKEY+'/25.8103146,-80.1751609,'+str(timestamp+(86400*(i)))
    response = requests.get(req)
    if response.status_code == 200:
        net_tries = 0
        data = response.json()
        for d in fields:
            try:
                values.append(data['currently'][d])
            except:
                values.append(-1)
    else:
        print("Problem occured with fetching data. Gimme a sec I'll try again...", end="\r", flush=True)
        net_tries = net_tries + 1
        if net_tries == 20:
            break
        else:
            continue
    #Dump data in csv file
    with open('weather_data_miami_beach.csv', 'a', , newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(values)
    csvFile.close()
    #increment i & j
    i = i + 1
    j = j + 1
    #if j == max then wait until next day
    if j == COST:
        j = 1
        print("Reached max API calls therefore going to sleep for 24 Hrs...")
        time.sleep(88000)
    #if i == int((timestampE-timestamp)/86400) then break
    if i == int((timestampE-(timestamp+86400))/86400):
        break
print("Success!")

