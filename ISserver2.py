import time, linecache, re
from urllib.parse import urlsplit, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'
PORT_NUMBER = 9000

class MyHandler(BaseHTTPRequestHandler):
    tempChart = ''
    humidityChart = ''
    moistureChart = ''
    waterChart = ''
    new_respond = 0


    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print('self path', self.path)
        if self.path != '/reading' and self.path != '/favicon.ico' and self.path != '/android' and self.path !='/turnOn' and self.path !='/turnOnOrOff':
            query = urlsplit(self.path).query
            params = parse_qs(query)
            print('parameters from path-dictionary', params)
            temp_param = params.get('temperature', 'temperature not exist')
            hum_param = params.get('humidity', 'humidity not exist')
            moi_param = params.get('moisture', 'moisture not exist')
            wat_param = params.get('water', 'water level not exist')
            print('air temperature', temp_param)
            print('air humidity', hum_param)
            print('soil moister', moi_param)
            print('water level', wat_param)
            temp_time = time.strftime(", Year: %Y, Month: %m, Day: %d, Hour: %H, Min: %M, Sec: %S", time.gmtime())
            print('temporary time', temp_time)
            data_temp = open('data.txt', 'at', encoding='utf8')
            data_temp.write('\n')
            data_temp.write('temperature: ')
            data_temp.writelines(temp_param)
            data_temp.write(', humidity: ')
            data_temp.writelines(hum_param)
            data_temp.write(', moisture: ')
            data_temp.writelines(moi_param)
            data_temp.write(', water: ')
            data_temp.writelines(wat_param)
            data_temp.writelines(temp_time)
            data_temp.close()
            self.respond_save()
        elif self.path == '/reading':
            temp_file = open('data.txt', 'r' )
            for line in temp_file:
                temp1_last_row = line
            temp_file.close()
            temp_last_row=temp1_last_row.rstrip("\n")
            print('temporary last row', temp_last_row)
            keys = re.split(": ?\w*,? ?", temp_last_row)
            values = re.split(",? ?\w*: ?", temp_last_row)
            keys.remove('')
            values.remove('')
            print('keys', keys)
            print('values', values)
            pairs=zip(keys,values)
            read_params_dict = dict(pairs)
            print('new dictionary with values', read_params_dict)
            tempChart = read_params_dict.get('temperature', 'temperature not exist')
            humidityChart = read_params_dict.get('humidity', 'humidity not exist')
            moistureChart = read_params_dict.get('moisture', 'moisture not exist')
            waterChart = read_params_dict.get('water', 'water level not exist')
            self.respond_load(tempChart, humidityChart, moistureChart, waterChart)
            tempChart= 0
            humidityChart =0
            moistureChart=0
            waterChart=0
        elif self.path == '/android':
            temp_file = open('data.txt', 'r')
            for line in temp_file:
                temp1_last_row = line
            temp_file.close()
            temp_last_row = temp1_last_row.rstrip("\n")
            print('temporary last row', temp_last_row)
            keys = re.split(": ?\w*,? ?", temp_last_row)
            values = re.split(",? ?\w*: ?", temp_last_row)
            keys.remove('')
            values.remove('')
            print('keys', keys)
            print('values', values)
            pairs = zip(keys, values)
            read_params_dict = dict(pairs)
            print('new dictionary with values', read_params_dict)
            tempChart = read_params_dict.get('temperature', 'temperature not exist')
            humidityChart = read_params_dict.get('humidity', 'humidity not exist')
            moistureChart = read_params_dict.get('moisture', 'moisture not exist')
            waterChart = read_params_dict.get('water', 'water level not exist')
            self.respond_android(tempChart, humidityChart, moistureChart, waterChart)
            tempChart = 0
            humidityChart = 0
            moistureChart = 0
            waterChart = 0
        elif self.path == '/turnOn':
            data_temp = open('pump.txt', 'w', encoding='utf8')
            data_temp.write('on')
            data_temp.close()
            self.respond_save_pump_on()
        elif self.path == '/turnOnOrOff':
            temp_file = open('pump.txt', 'r')
            # temp1_last_row = linecache.getline('data.txt', count)
            temp_pump = temp_file.readline()
            temp_file.close()
            if temp_pump == 'on':
                data_pump = open('pump.txt', 'w', encoding='utf8')
                data_pump.write('off')
                data_pump.close()
            self.respond_save_pump_onOrOff(temp_pump)

        else:
            self.respond()



    def handle_http(self, path):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
        <html><head><title>Irrigation system for potted plants.</title></head>
        <body><p>This is a test. Irrigation system for potted plants.</p>
        <p>You accessed path: {}</p>
        </body></html>
        '''.format(path)
        return bytes(content, 'UTF-8')


    def respond(self):
        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = 'something is wrong, try again'
        self.wfile.write(bytes(content, 'UTF-8'))


    def respond_save(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = 'saving data in data.txt'
        self.wfile.write(bytes(content, 'UTF-8'))
        response = self.handle_http(self.path)
        self.wfile.write(response)

    def respond_save_pump_on(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = 'pump will be turn on'
        self.wfile.write(bytes(content, 'UTF-8'))
        response = self.handle_http(self.path)
        self.wfile.write(response)

    def respond_save_pump_onOrOff(self, pumpValue):
        if pumpValue == 'on':
            new_respond = 201
        elif pumpValue == 'off':
            new_respond = 202
        else:
            new_respond = 203
        self.send_response(new_respond)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = 'checking data in pump.txt'
        self.wfile.write(bytes(content, 'UTF-8'))
        response = self.handle_http(self.path)
        self.wfile.write(response)

    def respond_load(self, tempChart, humidityChart, moistureChart, waterChart):
        # reading status is 200
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
                    <html>
                        <head>
                            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
                            <script type="text/javascript">
                                google.charts.load('current', {'packages':['table']});
                                google.charts.setOnLoadCallback(drawTable);

                                function drawTable() {
                                    var data = new google.visualization.DataTable();
                                    data.addColumn('string', 'Parameters');
                                    data.addColumn('string', 'Value');
                                    data.addRows([
                                    ['Temperature', ' ''' + tempChart + ''' C'],
                                    ['Humidity',  ' ''' + humidityChart + ''' %'],
                                    ['Moisture', ' ''' + moistureChart + ''' %'],
                                    ['Water level', ' ''' + waterChart + ''' %']
                                ]);

                                var table = new google.visualization.Table(document.getElementById('table_div'));

                                table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
                                }
                            </script>
                        </head>
                        <body>
                        <div id="table_div"></div>
                        </body>
                    </html>
                '''
        self.wfile.write(bytes(content, 'UTF-8'))
        response = self.handle_http(self.path)
        self.wfile.write(response)

    def respond_android(self, temp_android, humidity_android, moisture_android, water_android):
        # save status is 200
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
        <html><head><title>Irrigation system for potted plants.</title></head>
        <body><p>=temperature&''' + temp_android + '''&humidity&''' + humidity_android + '''&moisture&''' + moisture_android + '''&water&''' + water_android + '''=</p>
        <p>You accessed path: {}</p>
        </body></html>
        '''
        self.wfile.write(bytes(content, 'UTF-8'))
        response = self.handle_http(self.path)
        self.wfile.write(response)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class(('', PORT_NUMBER), MyHandler)
    print('time start',time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('time end', time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))