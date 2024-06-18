import psutil 
import requests
from itertools import count 
cputemp = [] 
for i in count(0):

       print("CPU_temp : ",psutil.sensors_temperatures().get('cpu_thermal')[0].current)
       cputemp.append(psutil.sensors_temperatures().get('cpu_thermal')[0].current)
       if len(cputemp) > 100:
                     cputemp.remove(cputemp[0])
       try:
            data = {"kornbot380@hotmail.com":{"Environment_sensor":{"cpu_temp_1":cputemp}}}
            #res = requests.post("http://192.168.50.192:5899/sensor_request",json=data)
            res = requests.post("https://roboreactor.com/sensor_request",json=data)
       except:
           print("Server error connection")            
        
