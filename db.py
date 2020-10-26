import mysql.connector
import datetime

import logging

logging.basicConfig(filename='log/db.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

mydb = mysql.connector.connect(
    host="localhost",
    user="pi",
    passwd="password",
    database="doma"
)


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

def saveMeasureToDB(dict={}):
    '''
    Shranjevanje meritve v bazo

    :param dict:  { 't1: 23, 't2': 54 ... }
    :return: 1 -> OK, 0-> ERROR
    '''
    mycursor = mydb.cursor()
    #for meritev in dict:
    #    device =
    sql = "insert into   doma.meritev (device_id,value, value_type,status, user ) values (%s,%s,%s, 1, 1)"
    val = ('t1', 20, 1)
    #mycursor.callproc('addMeritev', ['t1',20])
    #mycursor.stored_results()
    mydb.commit()
    #logging.info("INSERT:  " + str(name) + " ; " + str(val) + " ; ")
    return 1
