import datetime
import json
import time
from mqtt_client import MqttClient
from Scheduler import Scheduler
from MyThread import MyThread
from IrrigationFSM import IrrigationFSM



def save_schedulers_to_json(schedulers, filename):
    with open(filename, 'w',encoding="utf-8") as file:
        json.dump(schedulers, file, indent=4,ensure_ascii=False)

def load_schedulers_from_json(filename):
    with open(filename, 'r',encoding="utf-8") as file:
        return json.load(file)
    
    

class SchedulerManager:
    def __init__(self):
        self.schedulers = None
        self.is_running = False
        self.mqtt_client = MqttClient("192.168.1.7", 1883)
        self.mqtt_client.subscribe("add-schedule")
        self.mqtt_client.subscribe("update-schedule")
        self.mqtt_client.set_callback(self.custom_callback)
    def custom_callback(self,client, userdata, msg):
        if msg.topic == "add-schedule":
            print(msg.payload.decode())
            data = json.loads(msg.payload.decode())
            self.create_scheduler(data)
          
        if msg.topic == "update-schedule":
            print(msg.payload.decode())
            data = json.loads(msg.payload.decode())
            schedulers=self.get_all_schedulers()
            for scheduler in schedulers:
                if scheduler["id"] == data["id"]:
                    scheduler["isActive"] = data["isActive"]
                    break
            save_schedulers_to_json(schedulers,"schedulers.json")
    def create_scheduler(self, data):
        scheduler = Scheduler(data)
        self.schedulers = self.get_all_schedulers()
        self.schedulers.append(scheduler.to_dict())
        save_schedulers_to_json(self.schedulers,"schedulers.json")

    def update_scheduler(self, scheduler_name, data):
        for scheduler in self.schedulers:
            if scheduler.scheduler_name == scheduler_name:
                # Update the scheduler attributes
                if "cycle" in data:
                    scheduler.cycle = data["cycle"]
                if "flow1" in data:
                    scheduler.flow1 = data["flow1"]
                if "flow2" in data:
                    scheduler.flow2 = data["flow2"]
                if "flow3" in data:
                    scheduler.flow3 = data["flow3"]
                if "isActive" in data:
                    scheduler.is_active = data["isActive"]
                if "startTime" in data:
                    scheduler.start_time = datetime.datetime.strptime(data["startTime"], "%H:%M")
                if "stopTime" in data:
                    scheduler.stop_time = datetime.datetime.strptime(data["stopTime"], "%H:%M")
                break

    def delete_scheduler(self, scheduler_name):
        self.schedulers = [scheduler for scheduler in self.schedulers if scheduler.scheduler_name != scheduler_name]

    def get_all_schedulers(self):
        return load_schedulers_from_json("schedulers.json")
    def start_execution(self):
        schedulers_runing = []
        self.is_running = True
        while self.is_running:
            current_time = datetime.datetime.now().time().strftime("%H:%M")
            self.schedulers = self.get_all_schedulers()
            
            for scheduler in self.schedulers:      
                if scheduler["startTime"] == current_time and not any(scheduler_runing["id"] == scheduler["id"] for scheduler_runing in schedulers_runing):
                    thread = MyThread(target=self.run_scheduler,args=scheduler)
                    thread.start()
                    
                    schedulers_runing.append({"id":scheduler["id"],"thread":thread})
                    
                    print("Executing scheduler:"+ scheduler["schedulerName"] +" at " + str(datetime.datetime.now()))
                if scheduler["stopTime"] == current_time:
                    for scheduler_runing in schedulers_runing:
                        if scheduler_runing["id"] == scheduler["id"]:
                            print(scheduler_runing["thread"])
                            thread = scheduler_runing["thread"]
                            thread.stop()
                            thread.join()
                            schedulers_runing.remove(scheduler_runing)
                    
            time.sleep(1)
    def run_scheduler(self,scheduler,stop_flag):
        fsm = IrrigationFSM(scheduler)
        fsm.run(stop_flag=stop_flag)
    def stop_execution(self):
        self.is_running = False
        
if __name__ == "__main__":
    schedulerManager = SchedulerManager()
    schedulerManager.start_execution()