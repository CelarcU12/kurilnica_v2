# -*- coding: utf-8 -*-

import mysql.connector

import datetime

import logging

from Kurilnica import Kurilnica

#logging.basicConfig(filename='log/db.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
  #                  level=logging.DEBUG)
try:
    mydb = mysql.connector.connect(
        host="192.168.64.117",
        user="pi",
        passwd="password",
        database="doma"
    )
except:
    print("Error mzsql connect error")


def saveTempToDB(name, val):
    mycursor = mydb.cursor()
    if name == "T1":
        dev_id = 1
    elif name == "T2":
        dev_id = 2
    else:
        dev_id = 0
    sql = "INSERT INTO temperatura (name,value,device_id) VALUES (%s,%s,%s)"
    val = (name, val, dev_id)
    mycursor.execute(sql, val)
    mydb.commit()
    logging.info("INSERT:  " + str(name) + " ; " + str(val) + " ; ")


def saveRelayStatus(name, val, t1, t2):
    mycursor = mydb.cursor()
    val_num = 0
    relay_id = 0
    if val == "ON":
        val_num = 1
    if name == "peč":
        relay_id = 1

    sql = "insert into relayStatus (relay_id, name, t1, t2, status, status_id) values (%s,%s,%s,%s,%s,%s)"
    val = (1, name, t1, t2, val, val_num)
    mycursor.execute(sql, val)
    mydb.commit()
    logging.info("INSERT:  " + str(name) + " ; " + str(val) + " ; ")


def getData(tablename, name, from_, to):
    mycursor = mydb.cursor()
    sql = "SELECT * from " + tablename + " where name=%s AND time > %s AND time < %s"
    val = (name, from_, to)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    sez = []
    for x in myresult:
        sez.append(x)
    return sez


def getJsonData(tablename, name, from_, to):
    mycursor = mydb.cursor()
    sql = "SELECT * from " + tablename + " where name=%s AND time > %s AND time < %s"
    val = (name, from_, to)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    sez = []
    for el in myresult:
        sez.append({"name": el[4],
                    "vrednost": str(el[3]),
                    "cas": str(el[1])})
    return sez


def getMax(name, day=0):
    mycursor = mydb.cursor()
    if day == 0:
        sql = "select name, time, max(value)  from temperatura where date(time) !=%s and name=%s;"
    else:
        sql = "select name, time, max(value)  from temperatura where date(time) =%s and name=%s;"
    val = (day, name)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return myresult[0]


def getMin(name, day=0):
    mycursor = mydb.cursor()
    if day == 0:
        sql = "select name, time, min(value)  from temperatura where date(time) !=%s and name=%s;"
    else:
        sql = "select name, time, min(value)  from temperatura where date(time) =%s and name=%s;"
    val = (day, name)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return myresult[0]


def getToday(name):
    mycursor = mydb.cursor()
    sql = "SELECT name, time, value FROM temperatura WHERE DATE(time) = DATE(NOW() - INTERVAL 1 DAY) and name='T1';"
    mycursor.execute(sql, name)
    myresult = mycursor.fetchall()
    sez = []
    for el in myresult:
        sez.append({"name": el[0],
                    "vrednost": str(el[2]),
                    "cas": str(el[1])})
    return sez


def urNazaj(name, ure):
    '''ur Nazaj -> ime termometra, stevilo ur
        Vrne podatke od tega trenutka za pa n ur nazaj'''
    i = int(ure)
    if (name == "T1" and i % 2 == 0):
        i -= 1
    mycursor = mydb.cursor()
    sql = "SELECT name, from_unixtime(unix_timestamp(sec_to_time((time_to_sec(time) DIV 60)*60))), value FROM temperatura WHERE time >= NOW() - INTERVAL %s HOUR and name=%s and id mod %s = 0 order by time;"
    val = (ure, name, i)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    sez = []
    for el in myresult:
        sez.append({"name": el[0],
                    "vrednost": str(el[2]),
                    "cas": str(el[1])})
    return sez


def dniNazaj(name, dni):
    '''dni Nazaj -> ime termometra, stevilo dni
        Vrne podatke od tega trenutka za pa n dni nazaj
        vsak 5ti podatek'''
    mycursor = mydb.cursor()
    sql = "SELECT name, time, value, id FROM temperatura WHERE time >= NOW() - INTERVAL %s DAY and name=%s and id mod 5 = 0 order by time;"
    val = (int(dni), name)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    sez = []
    for el in myresult:
        sez.append({"name": el[0],
                    "vrednost": str(el[2]),
                    "cas": str(el[1]),
                    "id:": str(el[3])})
    return sez


def relaySpremembe(limit):
    '''On/Off spremembe, ki so se dogajale na releyju'''
    mycursor = mydb.cursor()
    sql = "SELECT id,relay_id, name, t1, t2, status, status_id, time from relayStatus limit %s ;"
    val = limit
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    sez = []
    for el in myresult:
        sez.append({"id": el[0],
                    "name": str(el[2]),
                    "t1:": str(el[3]),
                    "t2:": str(el[4]),
                    "status:": str(el[5]),
                    "time:": str(el[7])})
    return sez

def saveMeasureToDB(sez=[]):
    '''
    Shranjevanje meritve v bazo

    :param dict:  { 't1: 23, 't2': 54 ... }
    :return: 1 -> OK, 0-> ERROR
    '''
    try:
        mycursor = mydb.cursor()
        for meritev in sez:
            print(meritev.id + " tip: "+ meritev.type)
            sql = "insert into   doma.meritev (device_id,value, value_type,status, user ) values (%s,%s,%s, 1, 1)"
            val = (meritev.id, meritev.value, meritev.type)
        # mycursor.callproc('addMeritev', ['t1',20])
            mycursor.execute(sql, val)
            mydb.commit()
    #sql = "INSERT INTO temperatura (name,value,device_id) VALUES (%s,%s,%s)"
    #val = (name, val, dev_id)

    #logging.info("INSERT:  " + str(name) + " ; " + str(val) + " ; ")
        return 1
    except:
        return 9

def getDeviceMesaure(device_id, st_dni=1, natancnost=10):
    mycursor = mydb.cursor()
    sql = "SELECT value, measure_time FROM doma.meritev where device_id = %s and measure_time >= now() - INTERVAL %s DAY and id mod %s = 0 order by measure_time desc;"
    val = (int(device_id), st_dni, natancnost * st_dni)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    sez = []
    for el in myresult:
        sez.append({"vrednost": str(el[0]),
                    "cas": str(el[1])})
    return sez

def getDeviceMesaureNew(device_id):
    mycursor = mydb.cursor()
    sql = "SELECT value, create_time FROM doma.device_"+str(device_id)+" where create_time >= now() - INTERVAL 1 DAY order by create_time desc;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    sez = []
    for el in myresult:
        sez.append({"vrednost": str(el[0]),
                    "cas": str(el[1])})
    return sez
#print(getDeviceMesaureNew(1))
def getDeviceMesaureHour(device_id, st_ur=1, natancnost=10):
    #print("st dni"+str(st_ur))
    mycursor = mydb.cursor()
    sql = "SELECT value, measure_time FROM doma.meritev where device_id = %s and measure_time >= now() - INTERVAL %s HOUR and id mod %s = 0 order by measure_time desc;"
    val = (int(device_id), st_ur, natancnost )
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    sez = []
    for el in myresult:
        sez.append({"vrednost": str(el[0]),
                    "cas": str(el[1])})
    return sez


def getDeviceMesaureAll(st_dni=1, natancnost=100):
    mycursor = mydb.cursor()
    sql = "select device_id, value, measure_time from meritev where measure_time in (select     m.measure_time    FROM doma.meritev m where measure_time >= now() - INTERVAL %s hour and id mod %s = 0 order by measure_time desc);"
    val = (st_dni, natancnost * st_dni)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    sez = []
    cas= myresult[0][2]
    meritveByTime=[]
    i=0
    for el in myresult:
        # print(str(cas) +"=="+ str(el[2]))
        # if cas == el[2]:
        #     i+=1
        #     print("je enak")
        #     meritveByTime.append((el[0],el[1]))
        # else:
        #     i+=1
        #     print("Ni enak")
        #     cas == el[2]
        #     meritveByTime.append(("cas",cas))
        #     meritveByTime.append((el[0],el[1]))
        #     sez.append(meritveByTime)
        #     meritveByTime = []
        # if i > 30:
        #     break
        sez.append((el[0], str(el[1]),str(el[2])))
    return sez


def getLastData():
    sql = 'SELECT m.device_id, d.full_name, d.comment, m.value, d.type, m.measure_time FROM doma.meritev m, doma.device d where m.device_id = d.device_id and measure_time > now() - interval 1 hour order by m.measure_time desc , m.device_id limit 7;'
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    sez = []
    for el in myresult:
        sez.append(Kurilnica(el[1],el[0],el[3],str(el[3])+el[4],el[5],el[4], el[2]))
    return sez

def saveDevice(device_id, value):
    mycursor = mydb.cursor()

    sql1 = "SELECT TIMESTAMPDIFF(MINUTE,DATE_FORMAT(max(create_time),'%Y-%m-%d %H:%i'),DATE_FORMAT(now(),'%Y-%m-%d %H:%i')) FROM doma.device_"+str(device_id)
    mycursor.execute(sql1)
    razlika = mycursor.fetchall()[0][0]
    if(razlika is None):
        sql = "insert into   doma.device_"+str(device_id)+" (value) values ("+str(value)+")"
        val = (float(value))
        # mycursor.callproc('addMeritev', ['t1',20])
        mycursor.execute(sql, val)
        mydb.commit()
    elif (razlika>0):
        sql = "insert into   doma.device_"+str(device_id)+" (value) values ("+str(value)+")"
        val = (float(value))
        # mycursor.callproc('addMeritev', ['t1',20])
        mycursor.execute(sql, val)
        mydb.commit()

def getLastData(tableName):
    sql = "SELECT * FROM "+tableName+" order by create_time desc LIMIT 1;"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    temp = mycursor.fetchall()[0][2]
    return temp

#print(getLastData("device_4"))