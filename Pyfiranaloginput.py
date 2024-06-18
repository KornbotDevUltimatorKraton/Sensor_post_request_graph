import time 
import pyfirmata 
import requests 
import itertools
board = pyfirmata.ArduinoMega("/dev/ttyACM0") 
data_sensor = [] 
data_sensor1 = [] 
data_sensor2 = [] 
data_sensor3 = [] 
SENSOR_PIN = 0 
sensor_pin1 = 1 
sensor_pin2 = 2 
sensor_pin3 = 3 
LED_PIN = 13
laser1 = board.get_pin('d:5:p')
it = pyfirmata.util.Iterator(board)
it.start()

board.analog[SENSOR_PIN].enable_reporting()
board.analog[sensor_pin1].enable_reporting()
board.analog[sensor_pin2].enable_reporting()
board.analog[sensor_pin3].enable_reporting()
#laser1 = board.get_pin('d:5:p')
#laser1.write(0.8)
for _ in itertools.count(): 
    light_level = board.analog[SENSOR_PIN].read()
    sensor_1 = board.analog[sensor_pin1].read()
    sensor_2 = board.analog[sensor_pin2].read()
    sensor_3 = board.analog[sensor_pin3].read()
    if light_level != None: 
       print("Reading from analog sensor:",light_level,sensor_1,sensor_2,sensor_3)

       data_sensor.append(light_level)
       data_sensor1.append(sensor_1)
       data_sensor2.append(sensor_2)
       data_sensor3.append(sensor_3)
       if len(data_sensor) >= 100:
                   data_sensor.remove(data_sensor[0])
                   data_sensor1.remove(data_sensor1[0])
                   data_sensor2.remove(data_sensor2[0])
                   data_sensor3.remove(data_sensor3[0])
       
       laser1.write(0.6)
       data = {"kornbot380@hotmail.com":{"Chemical_sensor":{"sensor_1":data_sensor,"sensor_2":data_sensor1,"sensor_3":data_sensor2,"sensor_4":data_sensor3}}}
       print(data)
       try:
           #res = requests.post("http://0.0.0.0:8899/sensor_request",json=data)
           #res = requests.post("http://192.168.50.192:5899/sensor_request",json=data)
           res = requests.post("https://roboreactor.com/sensor_request",json=data)
       except:
           print("Server not found") 
       
    # EXERCISE add blinking of LEDs in response to reading
    # delay = ...
    # board.digital[LED_PIN].write(1)
    # board.pass_time(delay)
    # board.digital[LED_PIN].write(0)
    
