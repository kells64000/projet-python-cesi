# coding=utf-8
from bluepy.btle import Scanner, DefaultDelegate
import pymysql


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            if (dev.addr == 'd7:ef:13:27:15:29'):
                print ("Sensor externe découvert: ", dev.addr)
            if (dev.addr == 'd6:c6:c7:39:a2:e8'):
                print ("Sensor interne découvert: ", dev.addr)
        elif isNewData:
            if (dev.addr == 'd7:ef:13:27:15:29'):
                print ("Nouvelles données reçues depuis le sensor externe: ", dev.addr)
            if (dev.addr == 'd6:c6:c7:39:a2:e8'):
                print ("Nouvelles données reçues depuis le sensor interne:: ", dev.addr)

    def getDevicesData(devices):
        devicesDataList = []
        for dev in devices:
            currentDevice = []
            if (dev.addr == 'd7:ef:13:27:15:29' or dev.addr == 'd6:c6:c7:39:a2:e8'):
                currentDevice.append(dev.addr)
                print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
                for (adtype, desc, value) in dev.getScanData():
                    if (desc == 'Short Local Name'):
                        currentDevice.append(value)
                    if (desc == '16b Service Data'):
                        currentDevice.append(value)
                devicesDataList.append(currentDevice)
        return devicesDataList

    def formatToFloat(value):
        valueToDcl = str(int(value, 16))
        fomatValueToFloat = float(valueToDcl[:2] + "." + valueToDcl[2:])
        return fomatValueToFloat

    def formatDataBeforeInsert(devicesDataList):
        for deviceData in devicesDataList:
            if (len(deviceData) == 3):
                print('////////////////////////////////////')
                print('CURRENT DATA = ', deviceData)
                mac = deviceData[0]
                print('MAC ADRRESS = ', mac)
                name = deviceData[1]
                print('DEVICE NAME = ', name)
                id = deviceData[2][12:20]
                print('id = ', id)
                power = deviceData[2][20:22]
                print('Batterie = ', int(power, 16))
                formatTpt = ScanDelegate.formatToFloat(deviceData[2][24:28])
                print('Format tpt = ', formatTpt)
                formatHumidity = ScanDelegate.formatToFloat(deviceData[2][28:32])
                print('Format humidity = ', formatHumidity)
                ScanDelegate.insertSensor(name, mac, id, power, formatTpt, formatHumidity)

    def dbConnect():
        db = pymysql.connect("localhost", "pi", "python2019", "station-meteo")
        return db.cursor()

    def insertSensor(name, mac, id, power, tpt, humidity):
        cursor = ScanDelegate.dbConnect()
        # cursor.execute("TRUNCATE TABLE sensor")
        # sqlQuery = "INSERT INTO sensor (name, ID, Mac) VALUES (%s,%s,%s)"
        # sqlTuple = (name, id, mac);
        # cursor.execute(sqlQuery, sqlTuple)
        # cursor.execute("SELECT * FROM sensor")
        # data = cursor.fetchone()
        # print (data)

        # Récupération du censor id courrant
        sqlQuery = "SELECT id_sensor FROM sensor WHERE Mac = %s"
        sqlTuple = (mac)
        cursor.execute(sqlQuery, sqlTuple)
        data = cursor.fetchone()
        print("SENSOR ID")
        print(data)
        for row in data:
            cursor.close()
            ScanDelegate.insertDataSensor(row, power, tpt, humidity)

    def insertDataSensor(id, power, tpt, humidity):
        cursor = ScanDelegate.dbConnect()
        sqlQuery = "INSERT INTO data_sensor (date_releve, battery, temperature, humidity, id_sensor) VALUES (NOW(),%s,%s,%s,%s)"
        sqlTuple = (power, tpt, humidity, id);
        cursor.execute(sqlQuery, sqlTuple)
        cursor.close()
        return True;


################# MAIN #################

while True:
    # Création du scanner
    scanner = Scanner().withDelegate(ScanDelegate())
    # Récupération des sensors
    devices = scanner.scan(15.0)
    # Récupération des données envoyées par les sensors
    devicesDataList = ScanDelegate.getDevicesData(devices)
    # Formatage et insertion des datas
    ScanDelegate.formatDataBeforeInsert(devicesDataList)