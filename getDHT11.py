#!/usr/bin/python
import sys
import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11

while True:
    hum, temp = Adafruit_DHT.read_retry(sensor,4)
    print('Temp: {0:0.1f} C | Vlaga v zraku: {1:0.1f} %'.format(temp, hum))
    time.sleep(3)
