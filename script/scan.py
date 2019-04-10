from bluepy.btle import Scanner, DefaultDelegate
import pymysql
import requests
import json
from collections import namedtuple


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        dbSensors = DatabaseManager.getDatabaseDevices()
        # print (dbSensors)
        if isNewDev:
            if (dev.addr == dbSensors[1][3]):
                print("Sensor externe découvert: ", dev.addr)
            if (dev.addr == dbSensors[0][3]):
                print("Sensor interne découvert: ", dev.addr)
        elif isNewData:
            if (dev.addr == dbSensors[1][3]):
                print("Nouvelles données reçues depuis le sensor externe: ", dev.addr)
            if (dev.addr == dbSensors[0][3]):
                print("Nouvelles données reçues depuis le sensor interne:: ", dev.addr)

    def getSensorsData(dbSensors, scanSensors):
        sensorsDataList = []
        for scanSensor in scanSensors:
            currentSensor = []
            if (scanSensor.addr == dbSensors[0][3] or scanSensor.addr == dbSensors[1][3]):
                currentSensor.append(scanSensor.addr)
                print("Device %s (%s), RSSI=%d dB" % (scanSensor.addr, scanSensor.addrType, scanSensor.rssi))
                for (adtype, desc, value) in scanSensor.getScanData():
                    print("  %s = %s & ADTYPE = %s" % (desc, value, adtype))
                    if (desc == 'Short Local Name'):
                        currentSensor.append(value)
                    if (desc == '16b Service Data' and adtype == 22):
                        currentSensor.append(value)
                sensorsDataList.append(currentSensor)
        return sensorsDataList

    def formatToFloat(value):
        valueToDcl = str(int(value, 16))
        fomatValueToFloat = float(valueToDcl[:2] + "." + valueToDcl[2:])
        return fomatValueToFloat

    def formatDataBeforeInsert(devicesDataList):
        for deviceData in devicesDataList:
            print('DATA IN DEVICESDATA = ', len(deviceData))
            print('DEVICE DATA =', deviceData)
            if (len(deviceData) == 3):
                print('////////////////////////////////////')
                print('CURRENT DATA = ', deviceData)
                mac = deviceData[0]
                print('MAC ADRRESS = ', mac)
                power = deviceData[2][20:22]
                print('Batterie Hexa ', power)
                print('Batterie = ', int(power, 16))
                formatTpt = ScanDelegate.formatToFloat(deviceData[2][24:28])
                print('Format tpt = ', formatTpt)
                formatHumidity = ScanDelegate.formatToFloat(deviceData[2][28:32])
                print('Format humidity = ', formatHumidity)
                detectedSignal = True
                ScanDelegate.getSensorId(mac, power, formatTpt, formatHumidity, detectedSignal)
            else:
                mac = deviceData[0]
                power = None
                formatTpt = None
                formatHumidity = None
                detectedSignal = False
                ScanDelegate.getSensorId(mac, power, formatTpt, formatHumidity, detectedSignal)

    def getSensorId(mac, power, tpt, humidity, detectedSignal):
        cursor = DatabaseManager.dbConnect()

        # Récupération du censor id courrant
        sqlQuery = "SELECT id_sensor FROM sensor WHERE Mac = %s"
        sqlTuple = (mac)
        cursor.execute(sqlQuery, sqlTuple)
        ids = cursor.fetchone()
        print("SENSOR ID")

        for id in ids:
            cursor.close()
            ScanDelegate.insertDataSensor(id, power, tpt, humidity, detectedSignal)

    def insertDataSensor(id, power, tpt, humidity, detectedSignal):
        cursor = DatabaseManager.dbConnect()
        sqlQuery = "INSERT INTO data_sensor (date_releve, battery, temperature, humidity, detected_signal, id_sensor) VALUES (NOW(),%s,%s,%s,%s,%s)"
        sqlTuple = (power, tpt, humidity, detectedSignal, id);
        cursor.execute(sqlQuery, sqlTuple)
        cursor.close()
        return True;


class DatabaseManager():
    def dbConnect():
        db = pymysql.connect("localhost", "pi", "python2019", "station-meteo")
        return db.cursor()

    def getDatabaseDevices():
        devices = []
        cursor = DatabaseManager.dbConnect()
        cursor.execute("SELECT * FROM sensor")
        return cursor.fetchall()

    def insertApiData(temperature, humidity, detected_signal, id_weather_api):
        cursor = DatabaseManager.dbConnect();
        sqlQuery = 'INSERT INTO data_weather_api (date_releve, temperature, humidity, detected_signal, id_weather_api) VALUES (NOW(), %s,%s,%s,%s)'
        sqlTuple = (temperature, humidity, detected_signal, id_weather_api)
        cursor.execute(sqlQuery, sqlTuple)


class APIManager():
    def getWeather():
        res = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?id=3031582&APPID=6b10008581272cd3cf7f27252a35748f')
        data = res.json()
        if (data['cod'] == 200):
            temp = round(data['main']['temp'] - 273.15, 2);
            DatabaseManager.insertApiData(temp, data['main']['humidity'], True, 2)
        else:
            DatabaseManager.insertApiData(None, None, False, 2)


################# MAIN #################

while True:
    # Récupérer météo open data
    APIManager.getWeather()

    # Récupération des infos sensors
    databaseSensors = DatabaseManager.getDatabaseDevices();

    # Création du scanner
    scanner = Scanner().withDelegate(ScanDelegate())

    # Récupération des sensors
    scanSensors = scanner.scan(10.0)

    # Récupération des données envoyées par les sensors
    devicesDataList = ScanDelegate.getSensorsData(databaseSensors, scanSensors)

    # Formatage et insertion des datas
    ScanDelegate.formatDataBeforeInsert(devicesDataList)
