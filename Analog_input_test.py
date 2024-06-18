import cv2
import json 
import requests
import pyfirmata
import numpy as np 
from PIL import Image 
from itertools import count
try:
  board = pyfirmata.ArduinoMega("/dev/ttyUSB0")
except:
    try:
      board = pyfirmata.ArduinoMega("/dev/ttyUSB1")
    except:
        print("Dedevice connected")
it = pyfirmata.util.Iterator(board)
it.start()

board.analog[0].enable_reporting()
board.analog[1].enable_reporting() 
board.analog[2].enable_reporting() 
board.analog[3].enable_reporting() 
board.analog[4].enable_reporting() 
board.analog[5].enable_reporting() 
board.analog[6].enable_reporting()
board.analog[7].enable_reporting()
conv_units = 10000.0
for r in count(0):
    a0 = int(float(board.analog[0].read() or 0)*622.558)
    a1 = int(float(board.analog[1].read() or 0)*622.558) 
    a2 = int(float(board.analog[2].read() or 0)*622.558) 
    a3 = int(float(board.analog[3].read() or 0)*622.558) 
    a4 = int(float(board.analog[4].read() or 0)*622.558)
    a5 = int(float(board.analog[5].read() or 0)*622.558)
    a6 = int(float(board.analog[6].read() or 0)*622.558)
    a7 = int(float(board.analog[7].read() or 0)*622.558)
    #print(a0,type(a0),a1,a2,a3,a4,a5,a6,a7)
    list_array = list((a0,a1,a2,a3,a4,a5,a6,a7))
    #print(list_array)
    #coff = np.asarray(list_array)
    #print(coff)
    array = np.array(list_array)
    print(array)
    array = array.astype(np.uint8)
    array = np.reshape(array, (4,2))
    print(array)
    ndarray_data = json.dumps({"sensor_1":array.tolist()}) 
    data_array = {"kornbot380@hotmail.com":{"Array_sensor":json.loads(ndarray_data)}}
    data_bio = {"kornbot380@hotmail.com":{"Biometric_sensor":json.loads(ndarray_data)}}
    try:
      #req_array = requests.post("http://192.168.50.192:5899/sensor_request",json=data_array)
      req_bio = requests.post("https://roboreactor.com/sensor_request",json=data_array)  
    except:
       print("Error accessing server")
    #im1 = cv2.resize(array,(320,280))
    #color_image = cv2.cvtColor(array, cv2.COLOR_GRAY2RGB)*255
    #im2 = cv2.resize(color_image,(320,280))
    #color_image = Image.fromarray(np.uint8(array))
    #cv2.imshow("Sensor_array_image",im1)
    #cv2.imshow("Color visualize image",im2)
    #if cv2.waitKey(1) & 0xFF == ord(' '):
    #     break
#cv2.destroyAllWindows()
    # EXERCISE add blinking of LEDs in response to reading
    # delay = ...
    # board.digital[LED_PIN].write(1)
    # board.pass_time(delay)
    # board.digital[LED_PIN].write(0)
