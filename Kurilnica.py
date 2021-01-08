#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import json

class Kurilnica():
    def __init__(self, name="", id=0, lastValue=0, lastStrVal="OFF", lastTime=time.time(), type='celzija', comment='', razlika=0 ):
        self.name = name
        self.id = id
        self.value = lastValue
        self.strVal = lastStrVal
        self.time = lastTime
        self.type=type
        self.comment = comment
        self.razlika = razlika
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        print("Kurilnica  ime:"+self.name+" value " + str(self.value )+" time: "+str(self.time))


