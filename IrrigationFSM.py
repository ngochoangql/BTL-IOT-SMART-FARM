
import time
import minimalmodbus


# Thiết lập thông số kết nối Modbus
port = '/dev/ttyUSB0'  # Cổng COM ảo hoặc thực tế
baudrate = 9600

# Khởi tạo kết nối Modbus cho từng thiết bị
def init_modbus_device(port, slave_address):
    instrument = minimalmodbus.Instrument(port, slave_address)
    instrument.serial.baudrate = baudrate
    instrument.serial.timeout = 1
    return instrument

# Địa chỉ các thiết bị
device_ids = {
    'fertilizer_mixer_1': 1,
    'fertilizer_mixer_2': 2,
    'fertilizer_mixer_3': 3,
    'area_selector_1': 4,
    'area_selector_2': 5,
    'area_selector_3': 6,
    'pump_in': 7,
    'pump_out': 8
}

# Khởi tạo các thiết bị
devices = {name: init_modbus_device(port, id) for name, id in device_ids.items()}

def turn_on_device(device):
    device.write_bit(0, True)  # Bật relay (địa chỉ coil 0)

def turn_off_device(device):
    device.write_bit(0, False)  # Tắt relay (địa chỉ coil 0)

def stop_all_devices():
    for device in devices.values():
        turn_off_device(device)
class IrrigationFSM:
    def __init__(self, schedule):
        self.state = 'IDLE'
        self.schedule = schedule
        self.sensor1 = True
        self.sensor2 = True
        self.sensor3 = True
        print("**************************************************************")
        print("New FSM")

    def transition(self, new_state):
        print(f'Transitioning from {self.state} to {new_state}')
        self.state = new_state

    def run(self,stop_flag):
        self.flag = stop_flag
        prev_time = time.time()
        cycle = 0
        count = 0
        while True:
            current_time = time.time()
            if current_time - prev_time >= 1:
                prev_time = current_time
                if self.state == 'IDLE':
                    self.transition('MIXING1')
                        
                    
                elif self.state == 'MIXING1':
                    if count == 0 :
                        turn_on_device(devices['fertilizer_mixer_1'])
                        print(f'Mixing fertilizer 1 for {self.schedule["flow1"]}ml...')
                    else: 
                        
                        print(count)
                        if count == 10 or self.sensor1 == True:
                            self.transition('MIXING2')
                            print('Done mixing fertilizer 1')
                            turn_off_device(devices['fertilizer_mixer_1'])
                            count = 0
                    count +=1    
                    
                elif self.state == 'MIXING2':
                    if count == 0 :
                        turn_on_device(devices['fertilizer_mixer_2'])
                        print(f'Mixing fertilizer 2 for {self.schedule["flow2"]}ml...')
                    else: 
                        
                        print(count)
                        if count == 10 or self.sensor2 == True:
                            self.transition('MIXING3')
                            print('Done mixing fertilizer 2')
                            turn_off_device(devices['fertilizer_mixer_2'])
                            count = 0
                    count +=1  
                elif self.state == 'MIXING3':
                    if count == 0 :
                        turn_on_device(devices['fertilizer_mixer_3'])
                        print(f'Mixing fertilizer 3 for {self.schedule["flow3"]}ml...')
                    else: 
                        
                        print(count)
                        if count == 10 or self.sensor3 == True:
                            self.transition('PUMP_IN')
                            print('Done mixing fertilizer 3')
                            turn_off_device(devices['fertilizer_mixer_3'])
                            count = 0
                    count +=1  
                elif self.state == 'PUMP_IN':
                    
                    if count == 0 :
                        turn_on_device(devices['pump_in'])
                        print('Pumping in water...')
                    else: 
                        
                        print(count)
                        if count == 20 or self.sensor1 == True:
                            print('Done pumping in water')
                            self.transition('SELECTOR')
                            turn_off_device(devices['pump_in'])
                            count = 0
                    count +=1
                elif self.state == 'SELECTOR':
                    
                    if count == 0 :
                        print('Selecting area...')
                    else: 
                        print(count)
                        if count == 10 or self.sensor1 == True:
                            print('Done selecting area')
                            self.transition('PUMP_OUT')
                            count = 0
                    count +=1
                elif self.state == 'PUMP_OUT':
                    
                    if count == 0 :
                        turn_on_device(devices['pump_out'])
                        print('Pumping out water...')
                    else: 
                        
                        print(count)
                        if count == 20 or self.sensor1 == True:
                            print('Done pumping out water')
                            self.transition('NEXT_CYCLE')
                            turn_off_device(devices['pump_out'])
                            count = 0
                    count +=1
                elif self.state == 'NEXT_CYCLE':
                   
                    if cycle < self.schedule['cycle']-1:
                        if count == 0 :
                            print('Waiting for next cycle...')
                        else: 
                            
                            print(count)
                            if count == 10 or self.sensor1 == True:
                                print('Done pumping out water')
                                self.transition('MIXING1')
                                count = 0
                                cycle+=1
                        count +=1
                    else:
                        print('The end of irrigation.')
                        print("**************************************************************")
                        stop_all_devices()
                        self.flag.set()
                        break
                if stop_flag.is_set():
                    print('The end of irrigation.')
                    print("**************************************************************")
                    stop_all_devices()
                    break    