import markdown
import json

import os
from flask import Flask, escape, request,jsonify,Response
import sys

import random
import datetime
from Kurilnica import Kurilnica




#from relay import getStatus, on, off

import logging
#logging.basicConfig(filename='log/api.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

app = Flask(__name__)

temp1 = Kurilnica("Temp1", 1)
temp2 = Kurilnica("Temp2", 2)

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
<p>Zadnja meritev: '''+ str(temp4.time) +'''</p>


<br>
<h2>Temperatura : '''+ str(temp4.value) +'''</h2>
<br>

<br>
<h2>Vlaga : '''+ str(temp5.value) +'''</h2>
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
    <td>''' + str(temp1.value) + '''</td>
  </tr>
  <tr>
    <td>T2</td>
    <td>Zalogovnik</td>
    <td>'''+ str(temp2.value) +'''</td>
  </tr>
  <tr>
    <td>T3</td>
    <td>Peč</td>
    <td>'''+ str(temp3.value) +'''</td>
  </tr>
</table>
<a href="https://www.w3schools.com">This is a link</a>

</body>
</html>
'''
t1=[]
temp1 = Kurilnica("Temp1", 1)
temp2 = Kurilnica("Temp2", 2)
temp3 = Kurilnica("Temp3", 3)
temp4 = Kurilnica("Temp4", 4)
vlaga = Kurilnica("Vlaga", 5)
@app.route('/')
def hello():
    '''dokumentcija '''
    logging.info(" domov ")
    return html
    #return "<h1>Hello</h1>" \
     #      "<p> * T1: bojler:    "  +str(temp1.value)+temp1.strVal+"</p>"\
    ##      "<p> * T2: zalogovnik:   "+str(temp2.value)+temp2.strVal+"</p>"\
    #        "<p> * T3: peč :     "+str(temp3.value)+temp3.strVal+" </p>"

if __name__=='__main__':
    app.run(host='0.0.0.0')