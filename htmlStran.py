#HTML stran

import graf




def getHtml(t1, t2, t3, t4, v, r1, r2):

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


<h2>Pumpa med pečjo in zalogovnikom : '''+ str(r1.strVal) +'''</h2>
<a href='/r1=OFF'> OFF </a>
<a href='http://192.168.64.117:5000/r1=ON'> ON</a>
<h2>Pumpa za stanovanje : '''+ str(r2.strVal) +'''</h2>
<a href='http://192.168.64.117:5000/r2=OFF'> OFF </a>
<a href='http://192.168.64.117:5000/r2=ON'> ON</a>
<br>
<br>
<table style="width:90%">
  <tr>
    <th></th>
    <th>Naprava</th> 
    <th>Stopinj</th>
    <th>Razlika  </th>
  </tr>
  <tr>
    <td>T1</td>
    <td>BOJLER</td>
    <td>''' + str(t1.value) + '''</td>
    <td>''' + str(t1.razlika) + '''</td>
  </tr>
  <tr>
    <td>T2</td>
    <td>Zalogovnik</td>
    <td>'''+ str(t2.value) +'''</td>
    <td>''' + str(t2.razlika) + '''</td>
  </tr>
  <tr>
    <td>T3</td>
    <td>Peč</td>
    <td>'''+ str(t3.value) +'''</td>
    <td>''' + str(t3.razlika) + '''</td>
  </tr>
</table>
<h1> GRAFI </h1>
<div style="position: relative; width: 90%;">
<a> BOJLER</a>
'''+ graf.getGrafById(1)+ '''
<a> ZALOGOVNIK</a>
'''+ graf.getGrafById(2)+ '''
<a> PEC</a>
'''+ graf.getGrafById(3)+ '''
</div>
</body>
</html>
'''
    return html