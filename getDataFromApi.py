from logging import exception
import urllib.request, json
import sys

import db

lokacija= sys.argv[1]
# "http://192.168.64.116:8080/t"

def getData(apiUrl):
    try:
        res = urllib.request.urlopen(apiUrl)
        print(res.getcode())
        if(res.getcode() != 200):
            raise exception ("Url: "+ apiUrl + " ni dosegljiv")
        else:
            data = json.loads(res.read().decode())
            return data
    except:
        raise Exception("Prišlo je do napake getData("+apiUrl+")")

    

def saveToDB():
    print(lokacija)
    data = getData(lokacija)
    db.saveDevice(4,data['temp'])
    db.saveDevice(5,data['hum'])

saveToDB()
