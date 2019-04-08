from flask import Flask, render_template
import pymysql
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event

app = Flask(__name__)
#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()
id_dernier = 0

host = "127.0.0.1"
user = "pi"
password = "python2019"
db = "station-meteo"

class Database:
    def __init__(self):

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
    def getLastDataSensor(self):
        self.cur.execute("SELECT s.id_sensor, s.name,s.ID,s.Mac,ds.battery,ds.temperature,ds.humidity FROM data_sensor as ds  LEFT JOIN sensor  as s on s.id_sensor = ds.id_sensor ORDER BY id_data_sensor DESC LIMIT 2")
        result = self.cur.fetchall()
        id_dernier = result[0]["id_sensor"]
        return result
    def getSensor(self,id_sensor):
        self.cur.execute("SELECT s.id_sensor, s.name,s.ID,s.Mac,ds.battery,ds.temperature,ds.humidity FROM data_sensor as ds  LEFT JOIN sensor  as s on s.id_sensor = ds.id_sensor WHERE id_sensor = "+id_sensor)
        result = self.cur.fetchall()
        return result

class DataBaseThread(Thread):

    def __init__(self):
        self.delay = 1
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        global id_dernier  # Needed to modify global copy of globvar
        id_dernier = 0
        super(DataBaseThread, self).__init__()

    def getNewDataSensor(self):
        #infinite loop of magical random numbers
        while not thread_stop_event.isSet():
            self.cur.execute("SELECT s.id_sensor, s.name,s.ID,s.Mac,ds.battery,ds.temperature,ds.humidity FROM data_sensor as ds  LEFT JOIN sensor  as s on s.id_sensor = ds.id_sensor ORDER BY id_data_sensor DESC LIMIT 1")
            result = self.cur.fetchall()

            if result[0]["id_sensor"] != id_dernier:
                socketio.emit('getNewData', {
                    'id_sensor': result[0]["id_sensor"],
                    'name': result[0]["name"],
                    'ID': result[0]["ID"],
                    'Mac': result[0]["Mac"],
                    'battery': result[0]["battery"],
                    'temperature': str(result[0]["temperature"]),
                    'humidity': str(result[0]["humidity"])
                }, namespace='/test')

            DataBaseThread.set_globvar(result[0]["id_sensor"])

            sleep(self.delay)

    def run(self):
        self.getNewDataSensor()

    def set_globvar(glvar):
        global id_dernier  # Needed to modify global copy of globvar
        id_dernier = glvar

@app.route('/')
def employees():
    def db_query():
        db = Database()
        emps = db.getLastDataSensor()
        return emps
    res = db_query()
    return render_template('index.html', result=res, content_type='application/json')

@app.route('/sensor/<sensor_id>')
def sensor(sensor_id):
    db = Database()
    emps = db.getSensor(sensor_id)
    return render_template('data_sensor.html', result=emps, content_type='application/json')


@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    if not thread.isAlive():
        print("Starting Thread")
        thread = DataBaseThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)






