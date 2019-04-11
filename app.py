from flask import Flask, render_template
import pymysql
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
from flask_mail import Mail, Message

app = Flask(__name__)
#mail config
mail = Mail(app)

app.config['MAIL_SERVER']='localhost'
app.config['MAIL_PORT'] = 1035
# app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
# app.config['MAIL_PASSWORD'] = '*****'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()
id_dernier = 0

host = "192.168.43.58"
user = "pi"
password = "python2019"
db = "station-meteo"

class Database:
    def __init__(self):

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
    def getLastDataSensor(self):
        self.cur.execute("SELECT s.id_sensor, s.name,s.ID,s.Mac,ds.battery,ds.temperature,ds.humidity FROM (SELECT DISTINCT id_sensor, id_data_sensor,battery,temperature,humidity,date_releve FROM data_sensor ORDER BY id_data_sensor DESC) as ds  LEFT JOIN sensor  as s on s.id_sensor = ds.id_sensor GROUP BY s.id_sensor ORDER BY id_sensor LIMIT 3")
        result = self.cur.fetchall()
        id_dernier = result[0]["id_sensor"]
        return result
    def getSensor(self,id_sensor):
        self.cur.execute("SELECT s.id_sensor, s.name,s.ID,s.Mac,ds.battery,ds.temperature,ds.humidity,ds.date_releve FROM data_sensor as ds  LEFT JOIN sensor  as s on s.id_sensor = ds.id_sensor WHERE s.id_sensor = "+id_sensor+" ORDER BY ds.id_data_sensor DESC")
        result = self.cur.fetchall()
        return result
    def updateNameSensor(self,id_sensor,name_sensor):
        self.cur.execute("UPDATE `sensor` SET `name`= '"+name_sensor+"' WHERE `id_sensor` = "+id_sensor)
        result = self.cur.fetchall()
        return name_sensor
    def updateNameApi(self,id_api,name_api):
        self.cur.execute("UPDATE `weather_api` SET `name`= '"+name_api+"' WHERE `id_weather_api` = "+id_api)
        result = self.cur.fetchall()
        return name_api

class DataBaseThread(Thread):

    def __init__(self):
        self.delay = 5
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        global id_dernier  # Needed to modify global copy of globvar
        id_dernier = 0
        super(DataBaseThread, self).__init__()

    def getNewDataSensor(self):
        #infinite loop of magical random numbers
        while not thread_stop_event.isSet():
            self.cur.execute("SELECT s.id_sensor, s.name,s.ID,s.Mac,ds.id_data_sensor,ds.detected_signal,ds.battery,ds.temperature,ds.humidity,ds.date_releve FROM (SELECT DISTINCT id_sensor, id_data_sensor,detected_signal,battery,temperature,humidity,date_releve FROM data_sensor ORDER BY id_data_sensor DESC) as ds  LEFT JOIN sensor  as s on s.id_sensor = ds.id_sensor GROUP BY s.id_sensor ORDER BY id_sensor LIMIT 3")
            result = self.cur.fetchall()

            self.cur.execute("SELECT * FROM data_weather_api as dwa LEFT JOIN weather_api as wa on wa.id_weather_api = dwa.id_weather_api GROUP BY wa.id_weather_api ORDER BY dwa.id_data_weather_api DESC LIMIT 1")
            resultApi = self.cur.fetchall()

            if (len(result) >= 2 and resultApi != 0):
                socketio.emit('getNewData', {

                    'id_sensor': result[0]["id_sensor"],
                    'id_data_sensor': result[0]["id_data_sensor"],
                    'name': result[0]["name"],
                    'ID': result[0]["ID"],
                    'Mac': result[0]["Mac"],
                    'signal': result[0]["detected_signal"],
                    'battery': result[0]["battery"],
                    'temperature': str(result[0]["temperature"]),
                    'humidity': str(result[0]["humidity"]),
                    'date': str(result[0]["date_releve"].strftime('%d/%m/%Y %H:%M:%S')),

                    'id_sensor2': result[1]["id_sensor"],
                    'id_data_sensor2': result[1]["id_data_sensor"],
                    'name2': result[1]["name"],
                    'ID2': result[1]["ID"],
                    'Mac2': result[1]["Mac"],
                    'signal2': result[1]["detected_signal"],
                    'battery2': result[1]["battery"],
                    'temperature2': str(result[1]["temperature"]),
                    'humidity2': str(result[1]["humidity"]),
                    'date2': str(result[1]["date_releve"].strftime('%d/%m/%Y %H:%M:%S')),

                    'id_sensor3': resultApi[0]["id_weather_api"],
                    'id_data_sensor3': resultApi[0]["id_data_weather_api"],
                    'name3': resultApi[0]["name"],
                    #'ID3': resultApi[0]["ID"],
                    #'Mac3': resultApi[0]["Mac"],
                    'signal3': resultApi[0]["detected_signal"],
                    #'battery3': resultApi[0]["battery"],
                    'temperature3': str(resultApi[0]["temperature"]),
                    'humidity3': str(resultApi[0]["humidity"]),
                    'date3': str(resultApi[0]["date_releve"].strftime('%d/%m/%Y %H:%M:%S'))
                }, namespace='/getNewDataSensor')
            elif(len(result)>= 2):
                socketio.emit('getNewData', {

                    'id_sensor': result[0]["id_sensor"],
                    'id_data_sensor': result[0]["id_data_sensor"],
                    'name': result[0]["name"],
                    'ID': result[0]["ID"],
                    'Mac': result[0]["Mac"],
                    'signal': result[0]["detected_signal"],
                    'battery': result[0]["battery"],
                    'temperature': str(result[0]["temperature"]),
                    'humidity': str(result[0]["humidity"]),
                    'date': str(result[0]["date_releve"].strftime('%d/%m/%Y %H:%M:%S')),

                    'id_sensor2': result[1]["id_sensor"],
                    'id_data_sensor2': result[1]["id_data_sensor"],
                    'name2': result[1]["name"],
                    'ID2': result[1]["ID"],
                    'Mac2': result[1]["Mac"],
                    'signal2': result[1]["detected_signal"],
                    'battery2': result[1]["battery"],
                    'temperature2': str(result[1]["temperature"]),
                    'humidity2': str(result[1]["humidity"]),
                    'date2': str(result[1]["date_releve"].strftime('%d/%m/%Y %H:%M:%S'))
                }, namespace='/getNewDataSensor')
            elif(len(result) != 0):
                socketio.emit('getNewData', {

                    'id_sensor': result[0]["id_sensor"],
                    'id_data_sensor': result[0]["id_data_sensor"],
                    'name': result[0]["name"],
                    'ID': result[0]["ID"],
                    'Mac': result[0]["Mac"],
                    'signal': result[0]["detected_signal"],
                    'battery': result[0]["battery"],
                    'temperature': str(result[0]["temperature"]),
                    'humidity': str(result[0]["humidity"]),
                    'date': str(result[0]["date_releve"].strftime('%d/%m/%Y %H:%M:%S'))
                }, namespace='/getNewDataSensor')
            DataBaseThread.set_id_dernier(result[0]["id_sensor"])

            sleep(self.delay)

    def run(self):
        self.getNewDataSensor()

    def set_id_dernier(glvar):
        global id_dernier  # Needed to modify global copy of globvar
        id_dernier = glvar

#class Mail (Thread):

@app.route('/')
def index():
    def db_query():
        db = Database()
        emps = db.getLastDataSensor()
        return emps
    res = db_query()
    return render_template('index.html', result=res, content_type='application/json')

@app.route('/sensor/<sensor_id>' )
def sensor(sensor_id):
    db = Database()
    emps = db.getSensor(sensor_id)
    return render_template('data_sensor.html', result=emps, content_type='application/json')

@app.route('/sensorName/<sensor_id>/<sensor_name>', methods = ['POST'])
def sensorName(sensor_id,sensor_name):
    db = Database()
    emps = db.updateNameSensor(sensor_id,sensor_name)
    return emps

@app.route('/apiName/<api_id>/<api_name>', methods = ['POST'])
def apiName(api_id,api_name):
    db = Database()
    emps = db.updateNameApi(api_id,api_name)
    return emps

@socketio.on('connect', namespace='/getNewDataSensor')
def socket_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    if not thread.isAlive():
        print("Starting Thread")
        thread = DataBaseThread()
        thread.start()

@socketio.on('disconnect', namespace='/getNewDataSensor')
def socket_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
