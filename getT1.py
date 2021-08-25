import requests
import json

from posljiMail import posljiemail

r=requests.get('http://192.168.64.117/t1')

status=r.status_code
poslano = False
if (status != 200 and not poslano):
    posljiemail('furbek.celarc@gmail.com','Server status ERROR. Status code = '+str(status))
    poslano = True
else:
    json = r.json()
    if (json['vrednost'] < 40 and not poslano):
        print('Pošlji mai')
        posljiemail('furbek.celarc@gmail.com','Pod 40')
        poslano = True
    elif json['vrednost'] > 40:
        poslano = False
