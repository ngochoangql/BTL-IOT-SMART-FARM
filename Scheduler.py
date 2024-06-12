import datetime
import json
import time
import threading
import uuid
import asyncio
from mqtt_client import MqttClient



       
        
class Scheduler:
    def __init__(self, data):
        self.id = str(uuid.uuid4())
        self.cycle = data.get("cycle")
        self.flow1 = data.get("flow1")
        self.flow2 = data.get("flow2")
        self.flow3 = data.get("flow3")
        self.is_active = data.get("isActive")
        self.scheduler_name = data.get("schedulerName")
        self.start_time = datetime.datetime.strptime(data.get("startTime"), "%H:%M").time()
        self.stop_time = datetime.datetime.strptime(data.get("stopTime"), "%H:%M").time()

    def to_dict(self):
        return {
            "id":self.id,
            "cycle": self.cycle,
            "flow1": self.flow1,
            "flow2": self.flow2,
            "flow3": self.flow3,
            "isActive": self.is_active,
            "schedulerName": self.scheduler_name,
            "startTime": self.start_time.strftime("%H:%M"),
            "stopTime": self.stop_time.strftime("%H:%M")
        }

