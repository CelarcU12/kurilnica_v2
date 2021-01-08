# -*- coding: utf-8 -*-


#import markdown
import json

import os


from flask import Flask, escape, request,jsonify,Response, redirect
import sys

import random
import datetime
import time
from Kurilnica import Kurilnica
import db
import graf
import htmlStran as html


#from relay import getStatus, on, off

import logging
#logging.basicConfig(filename='log/api.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

app = Flask(__name__)


t1=[]
temp1 = Kurilnica("Temp1", 1)
temp2 = Kurilnica("Temp2", 2)
temp3 = Kurilnica("Temp3", 3)
temp4 = Kurilnica("Temp4", 4)
vlaga = Kurilnica("Vlaga", 5)
reley1 = Kurilnica("Relay1", 7, 0)
reley2 = Kurilnica("Relay2", 8, 0)


@app.route('/')
def hello():
    '''dokumentcija '''
    logging.info(" domov ")
    return html.getHtml(temp1,temp2,temp3,temp4,vlaga ,reley1,reley2)


@app.route('/getAll', methods=['GET'])
def getAll():
    content = request.json
    return jsonify({'name':'Kurilnica',
                    'vrednosti':t1
                    })

@app.route('/t1', methods=['GET'])
def getData1():
    content = request.json
    #t1 = Temp('Pec',getT1(),'28-0314977974ee', datetime.datetime.now())
    #logging.info('t1'+str(t1))

    return jsonify({'name':temp1.name,
                    'zadnja_meritev': temp1.time,
                    'vrednost':temp1.value
                    })

auto = 1 

zadnjaMeritev = datetime.datetime.now()
prvic = True
r1=0
r2=0
r3=0

def getZadnjaMeritev():
    return zadnjaMeritev

def preveriTemp1(temp1, temp2):
    if (temp1.value > temp3.value) and (temp3.razlika <= 0):
        return "OFF"
    elif (temp1.value <= temp3.value):
        return "ON"
    else:
        return "OFF"


@app.route('/t1', methods=['POST'])
def postData1():
    print("post T1")
    print(request.json)
    content = request.json
    v1= request.json['t1']
#    temp1.razlika = temp1.value - v1
    temp1.value =v1
    v2= request.json['t2']
#    temp2.razlika = temp2.value - v2
    temp2.value =v2
    v3= request.json['t3']
#    temp3.razlika = temp3.value - v3
    temp3.value =v3
    temp1.time = datetime.datetime.now()
    temp2.time = datetime.datetime.now()
    temp3.time = datetime.datetime.now()
    temp4.value = request.json['t4']
    temp4.time = datetime.datetime.now()
    vlaga.value = request.json['h4']
    vlaga.time = datetime.datetime.now()
    global zadnjaMeritev
    global prvic
    global r1, r2, r3
    razlika = datetime.datetime.now() - zadnjaMeritev
    
    if prvic:
        print("Razlika prvic")
        r1 = v1
        r2 = v2
        r3 = v3
        prvic = False
        print("Razlika prvic"+ str(r1))
    print(razlika.seconds)
    if razlika.seconds > 180:
        print("vec kot 180")
        zadnjaMeritev = temp1.time
        print(zadnjaMeritev)

        temp1.razlika = round(temp1.value - r1,2)
        temp2.razlika = round(temp2.value - r2,2)
        temp3.razlika = round(temp3.value - r3,2)
        r1 = temp1.value
        r2 = temp2.value
        r3 = temp3.value

    name1 = request.form.get('name1')
    autoStr=""
    if name1:
        auto = 1
        autoStr="Auto ON"
    else:
        auto = 0
        autoStr = "Auto OFF"

    reley1.strVal = preveriTemp1(temp1, temp3)

    t_cur = (temp1.value,temp2.value,temp3.value,temp4.value, vlaga.value, vlaga.time)
    t1.append(t_cur)

    db.saveMeasureToDB([temp1,temp2,temp3,temp4,vlaga,reley1,reley2])
    return jsonify({
        'las_val': datetime.datetime.now(),
        't1': t_cur,
        'all':t1[-1]
    }), 201


@app.route('/r1', methods=['GET'])
def relay1Get():
    return jsonify({'r1':reley1.value, 'value':reley1.strVal})
@app.route('/r1', methods=['POST'])
def relay1Post():
    '''
    status releja 1, 0 => OFF, 1=> ON
    '''
    print("post r1")
    print(request.json)
    #content = request.json
    reley1.value = request.json['r1']
    reley1.strVal = request.json['value']
    return jsonify({'r1':reley1.value,
                    'value':reley1.strVal
                    }), 201

@app.route('/r2', methods=['GET'])
def relay2Get():
    return jsonify({'r2':reley2.value})
@app.route('/r2', methods=['POST'])
def relay2Post():
    '''
    status releja 2, 0 => OFF, 1=> ON
    '''
    print("post r2")
    print(request.json)
    #content = request.json
    reley2.value = request.json['r2']
    reley2.strVal = request.json['value']
    return jsonify({'r2':reley2.value,
                    'value': reley2.strVal
                    }), 201
@app.route('/r1=<status>', methods=['GET'])
def relay1OnOffPost(status):
    '''
    status releja 2, 0 => OFF, 1=> ON
    '''
    print("post r1 "+status)
    reley1.strVal = status
    return redirect('/')
   # return jsonify({'r1':reley1.value,
    #                'value': reley1.strVal
     #               }), 201
@app.route('/r2=<status>', methods=['GET'])
def relay2OnOffPost(status):
    '''
    status releja 2, 0 => OFF, 1=> ON
    '''
    print("post r2 "+status)
    reley2.strVal = status
    return redirect('/')

@app.route('/relayStatus', methods=['GET'])
def relayStatus():
    return jsonify({'r1':reley1.strVal,
                    'r2':reley2.strVal})

@app.route('/devices=<device_id>', methods=['GET'])
def getDataOfDevice(device_id):
    content = request.json
    sez = db.getDeviceMesaure(device_id)
    return Response(json.dumps(sez), mimetype='application/json')

@app.route('/devices=<device_id>/hour=<hour>', methods=['GET'])
def getDataOfDeviceHour(device_id,hour):
    content = request.json
    sez = db.getDeviceMesaureHour(device_id, hour)
    print(len(sez))
    return Response(json.dumps(sez), mimetype='application/json')


@app.route('/device1', methods=['GET'])
def getDataOfDevice1():
    print("device 1")
    print(request.url)
    sez = db.getDeviceMesaure(1)
    return Response(json.dumps(sez), mimetype='application/json')

@app.route('/device2', methods=['GET'])
def getDataOfDevice2():
    content = request.json
    sez = db.getDeviceMesaure(2)
    return Response(json.dumps(sez), mimetype='application/json')
@app.route('/device3', methods=['GET'])
def getDataOfDevice3():
    content = request.json
    sez = db.getDeviceMesaure(3)
    return Response(json.dumps(sez), mimetype='application/json')

@app.route('/devices', methods=['GET'])
def getDataOfAllDevices():
    content = request.json
    sez = db.getDeviceMesaureAll()
    if len(sez) == 0:
        return jsonify({'prazen seznam'
                    }), 200
    cas= sez[0][2]
    res =[]
    one={}
    j=0
    for i in range(0,len(sez)):
        if cas != sez[i][2]:
            cas = sez[i][2]
            one['cas']= sez[i][2]
            one[sez[i][0]]= sez[i][1]
            res.append(one)
            one={}
            j+=1
        else:
            one[sez[i][0]]= sez[i][1]
    return Response(json.dumps(res),  mimetype='application/json')
#    return Response(json.dumps(sez), mimetype='application/json')

@app.route('/i', methods=['GET'])
def getInfoOfDevices():
    ''' dobi zadnje informacije o vseh napravah '''
    try:
        sez = db.getLastData()
    except:
        return 500
    
    res=[]
    for el in sez:
        res.append({
                'id': el.id,
                'ime': el.name,
                'vrednost': str(el.value),
                'tip': el.type,
                'zadnjaMeritev': str(el.time),
                'vrednostStr': el.strVal,
                'opis': el.comment
        })
           
    #return res
    return Response(json.dumps(res),  mimetype='application/json')
if __name__=='__main__':
    print("cakamo ................")
    time.sleep(1)
    print(" ........  zaganjamo .......")
    app.run(host='0.0.0.0', threaded=True)
    
        
        
