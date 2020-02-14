files = ['BelleGlade', 'BonitaSprings', 'CapeCoral', 'Goodland', 'HomesteadAirReserveBase', 'Immokalee', 'KingsPoint', 'LehighAcres', 'LibertyPoint', 'Turkeyfoot', 'WestPalmBeach']
for city in files:
    with open(city + '.csv', 'r') as input_file, open('weather_data_' + city +'.csv', 'w+') as output_file:
        output_file.write('time,summary,precipIntensity,precipProbability,temperature,apparentTemperature,dewPoint,humidity,pressure,windSpeed,windBearing,cloudCover,uvIndex,visibility,nearestStormDistance')
        for line in input_file:
            if not(line == "\n"):
                output_file.write(line)
        