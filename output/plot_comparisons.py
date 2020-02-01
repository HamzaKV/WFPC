import csv
import matplotlib.pyplot as plt

weatherDataParams = ['precipIntensity', 'precipProbability', 'temperature', 'humidity', 'pressure', 'windSpeed', 'windBearing']
times = []
forecastsLoc = []
weatherDataLoc = []

with open('../input/weather_data_miami.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line = 0
    paramIndices = []
    for row in csv_reader:
        if line == 0:
            for i in range(len(weatherDataParams)):
                if weatherDataParams[i] in row:
                    paramIndices.append(row.index(weatherDataParams[i]))
        else:
            times.append(int(row[0]))
            forecastsLoc.append(row[1])
            tmp = []
            for i in paramIndices:
                tmp.append(float(row[i]))
            weatherDataLoc.append(tmp)
        line = line + 1

nwpWeatherDataParams = ['temperature', 'windSpeed', 'windBearing']
nwpPredictedTimes = []
nwpPredictedWeather = []
with open('weather_nwp_miami.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        nwpPredictedTimes.append(int(row[0]))
        tmp = []
        for i in range(1, len(row)):
            tmp.append(float(row[i]))
        nwpPredictedWeather.append(tmp)
nwpWeatherDataParamsIndexs = []
for x in nwpWeatherDataParams:
    if x in weatherDataParams:
        nwpWeatherDataParamsIndexs.append(weatherDataParams.index(x))
realWeatherDatas = []
for i in range(times.index(nwpPredictedTimes[0]), times.index(nwpPredictedTimes[len(nwpPredictedTimes) - 1]) + 1):
    realWeatherDatas.append(weatherDataLoc[i])
nwpRealData = []
for r in realWeatherDatas:
    tmp = []
    for i in nwpWeatherDataParamsIndexs:
        tmp.append(r[i])
    nwpRealData.append(tmp)

plotNWPWeatherData = []
plotNWPPredictedData = []
wc = 0
while wc < len(nwpRealData[0]):
    tmp1 = []
    tmp2 = []
    for i in range(len(nwpRealData)):
        tmp1.append(nwpRealData[i][wc])
        tmp2.append(nwpPredictedWeather[i][wc])
    plotNWPWeatherData.append(tmp1)
    plotNWPPredictedData.append(tmp2)
    wc = wc + 1
for i in range(len(plotNWPWeatherData)):
    plt.figure(i+1)
    plt.subplot(211)
    plt.plot(nwpPredictedTimes, plotNWPWeatherData[i])
    plt.ylabel('actual ' + nwpWeatherDataParams[i])
    plt.subplot(212)
    plt.plot(nwpPredictedTimes, plotNWPPredictedData[i])
    plt.xlabel('date')
    plt.ylabel('predicted ' + nwpWeatherDataParams[i])
    plt.show()

predictedTimes = []
predictedForecasts = []
predictedWeather = []
with open('weather_sw_miami.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        predictedTimes.append(int(row[0]))
        predictedForecasts.append(row[1])
        tmp = []
        for i in range(2, len(row)):
            tmp.append(float(row[i]))
        predictedWeather.append(tmp)
realWeatherData = []
for i in range(times.index(predictedTimes[0]), times.index(predictedTimes[len(predictedTimes) - 1]) + 1):
    realWeatherData.append(weatherDataLoc[i])

plotWeatherData = []
plotPredictedData = []
wc = 0
while wc < len(realWeatherData[0]):
    tmp1 = []
    tmp2 = []
    for i in range(len(realWeatherData)):
        tmp1.append(realWeatherData[i][wc])
        tmp2.append(predictedWeather[i][wc])
    plotWeatherData.append(tmp1)
    plotPredictedData.append(tmp2)
    wc = wc + 1
for i in range(len(plotWeatherData)):
    plt.figure(i+1)
    plt.subplot(211)
    plt.plot(predictedTimes, plotWeatherData[i])
    plt.ylabel('actual ' + weatherDataParams[i])
    plt.subplot(212)
    plt.plot(predictedTimes, plotPredictedData[i])
    plt.xlabel('date')
    plt.ylabel('predicted ' + weatherDataParams[i])
    plt.show()
