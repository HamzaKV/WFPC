with open('weather_data_miami_hollywood.csv', 'r') as input_file, open('weather_data_miami_hollywood_temp.csv', 'w+') as output_file:
    for line in input_file:
        if not(line == "\n"):
            output_file.write(line)
        