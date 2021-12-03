#!/usr/bin/python3
# -*- coding: utf-8

# Izriši graf
# temperatura zadnjih n ur



import plotly.express as px
import db

#fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])

#div = fig.to_html(full_html=False) 
#print(div)

def getGrafDiv(x=[],y=[]):
    fig = px.line(x=x, y=y)
    fig.update_traces(mode='markers+lines')
    div = fig.to_html(full_html=False)
    return div


def getGrafById(device_id=1):
    try:
        js = db.getDeviceMesaure(device_id)
    except Exception as ex:
        return "<div> Težave z povezavo na baz  " + str(ex) + " </div>"
    if js==[]:
        return "<div> Napaka "+ str(ex)+ " </div>"
    x=[]
    y=[]
    for el in js:
        x.append(el['cas'])
        y.append(float(el['vrednost']))
    return getGrafDiv(x,y)
