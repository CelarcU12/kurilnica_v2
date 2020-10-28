import markdown
import json

import os
from flask import Flask, escape, request,jsonify,Response
import sys

import random
import datetime
from Kurilnica import Kurilnica


#import db

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

def getHtml(t1=temp1, t2=temp2, t3=temp3, t4=temp4, v=vlaga, r1=reley1, r2=reley2):
    html = '''<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 15px;
}
</style>
</head>
<body>

<h2>Kurilnica</h2>
<p>Zadnja meritev: '''+ str(t4.time) +'''</p>


<br>
<h2>Temperatura : '''+ str(t4.value) +'''</h2>
<br>

<br>
<h2>Vlaga : '''+ str(v.value) +'''</h2>
<br>
<br>
<h2>Pumpa med pečjo in zalogovnikom : '''+ str(r1.strVal) +'''</h2>
<h2>Pumpa za stanovanje : '''+ str(r2.strVal) +'''</h2>
<br>
<br>
<table style="width:100%">
  <tr>
    <th></th>
    <th>Naprava</th> 
    <th>Stopinj</th>
  </tr>
  <tr>
    <td>T1</td>
    <td>BOJLER</td>
    <td>''' + str(t1.value) + '''</td>
  </tr>
  <tr>
    <td>T2</td>
    <td>Zalogovnik</td>
    <td>'''+ str(t2.value) +'''</td>
  </tr>
  <tr>
    <td>T3</td>
    <td>Peč</td>
    <td>'''+ str(t3.value) +'''</td>
  </tr>
</table>
<a href="https://www.w3schools.com">This is a link</a>

</body>
</html>
'''
    return html
@app.route('/')
def hello():
    '''dokumentcija '''
    logging.info(" domov ")
    return getHtml(temp1,temp2,temp3,temp4,vlaga ,reley1,reley2)
    #return "<h1>Hello</h1>" \
     #      "<p> * T1: bojler:    "  +str(temp1.value)+temp1.strVal+"</p>"\
    ##      "<p> * T2: zalogovnik:   "+str(temp2.value)+temp2.strVal+"</p>"\
    #        "<p> * T3: peč :     "+str(temp3.value)+temp3.strVal+" </p>"


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


def preveriTemp1(temp1, temp2):
    if temp1.value > temp2.value:
        return "OFF"
    else
        return "ON"


@app.route('/t1', methods=['POST'])
def postData1():
    print("post T1")
    print(request.json)
    content = request.json
    temp1.value = request.json['t1']
    temp1.time = datetime.datetime.now()
    temp2.value = request.json['t2']
    temp2.time = datetime.datetime.now()
    temp3.value = request.json['t3']
    temp3.time = datetime.datetime.now()
    temp4.value = request.json['t4']
    temp4.time = datetime.datetime.now()
    vlaga.value = request.json['h4']
    vlaga.time = datetime.datetime.now()

    reley1.strVal = preveriTemp1(temp1, temp3)

    t_cur = (temp1.value,temp2.value,temp3.value,temp4.value, vlaga.value, vlaga.time)
    t1.append(t_cur)

    db.saveMeasureToDB([temp1,temp2,temp3,temp4,vlaga,reley1,reley2])
    return jsonify({
        'las_val': datetime.datetime.now(),
        't1': t_cur,
        'all':t1
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

@app.route('/relayStatus', methods=['GET'])
def relayStatus():
    return jsonify({'r1':reley1.strVal,
                    'r2':reley2.strVal})

if __name__=='__main__':
    app.run(host='0.0.0.0')