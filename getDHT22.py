import Adafruit_DHT

DS = Adafruit_DHT.DHT22
DP = 4

DP2 = 17
def getData(pin):
    while True:
        hum , temp = Adafruit_DHT.read_retry(DS, pin)
        if hum is not None and temp is not None:        
            print("Temp={0:0.1f} *c Hum ={1:0.1f}%".format(temp, hum))
            return hum, temp
        else:
            print("failed to read!")


getData(4)
getData(17)
