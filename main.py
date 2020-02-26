from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
from weather import WeatherApp

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        parsed_path = urlparse(self.path)
        querys = parsed_path.query.split('&')
        dataQuery = querys[0].split('=')
        dateQuery = querys[1].split('=')
        data1 = None
        date = None
        if dataQuery[0] == 'data':
            data1 = dataQuery[1]
        if dateQuery[0] == 'date':
            date = dateQuery[1]
        if data1 == 'fetch' and not(date is None):
            data = {}
            r = WeatherApp(['precipIntensity', 'precipProbability', 'temperature', 'humidity', 'pressure', 'windSpeed', 'windBearing']).run(int(date))
            data['method'] = 'GET'
            for i in range(len(r)):
                a = r[i]
                cityData = {}
                cityData['city'] = a[0]
                for j in range(len(a[1])):
                    d = (a[1][j][0]).split(',')
                    day = {}
                    day['time'] = d[0]
                    day['forecast'] = d[1]
                    day['precipIntensity'] = d[2] 
                    day['precipProbability'] = d[3]
                    day['temperature'] = d[4]
                    day['humidity'] = d[5]
                    day['pressure'] = d[6]
                    day['windSpeed'] = d[7]
                    day['windBearing'] = d[8]
                    cityData['day' + str(j)] = day
                data[str(i)] = cityData
            self.wfile.write(json.dumps(data).encode())

if __name__ == '__main__':
    with HTTPServer(('192.168.0.80', 8000), SimpleHTTPRequestHandler) as httpd:
        print('Server started...')
        httpd.serve_forever()

# http://localhost:8000/?data=fetch&date=1514696400
