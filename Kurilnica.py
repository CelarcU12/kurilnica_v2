import time
import json

class Kurilnica():
    def __init__(self, name="", id=0, lastValue=0, lastStrVal="OFF", lastTime=time.time(), type='celzija' ):
        self.name = name
        self.id = id
        self.value = lastValue
        self.strVal = lastStrVal
        self.time = lastTime
        self.type=type
    def to_JSON(self):
        return json.dump(self.__dict__)
    def __str__(self):
        print("Kurilnica  ime:"+self.name+" value " + self.value +" time: "+ self.time)


