import requests
from itertools import count 
for i in count(0):

   try:
      data = {"kornbot380@hotmail.com":{"Position_sensor":{"sensor_1":[1,23,4,5,6,100,230,300],'sensor_2':[23,40,200,230,450],'sensor_3':[3,56,1,30,40,50,600,700]}}}
      print("Position_data",data) 
      #res = requests.post("http://192.168.50.192:5899/sensor_request",json=data)
      res = requests.post("https://roboreactor.com/sensor_request",json=data)
   except:
      print("Error server connection")
