#!/usr/bin/python
import os 

import smbus
import math
import time  
import requests
from itertools import count 
from mpu6050 import mpu6050
# Initialize the MPU6050 sensor
sensor = mpu6050(0x68)
# Set the starting values for the Z angle
x_angle = y_angle = z_angle = 0
last_time = time.time()
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
AngleDegX  = 0 
AngleDegY = 0 
AngleDegZ = 0 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


os.system("sudo chmod -R 777 /dev/i2c-1") # give the permission to the i2c  device tree 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)
 
print("Gyroscope")
print("--------")
 
gyroskop_xout = read_word_2c(0x43)
gyroskop_yout = read_word_2c(0x45)
gyroskop_zout = read_word_2c(0x47)

# Accelleration 
accel_x = []
accel_y = [] 
accel_z = [] 

# Velocity_calculation 
velocity_x = [0]
velocity_y = [0]
velocity_z = [0]

# Distance_calculation 
position_x = [0] 
position_y = [0]
position_z = [0]

# Angle_data
Angle_x_dat = [] 
Angle_y_dat = [] 
Angle_z_dat = [] 
#Accel dat 
Accel_x_dat = [] 
Accel_y_dat = [] 
Accel_z_dat = [] 
def Distance_calculation(dt):
     
         def x_accel_data(dt): 
               if len(accel_x) >=2:
                  for i in range(0,len(accel_x)-1):
                       try:
                            vx = velocity_x[i-1] + (accel_x[i] + accel_x[i-1])*math.pow(2*dt,-1)                       
                            velocity_x.append(vx)
                       except:
                             print("Un available cal")      
                  for i in range(0,len(accel_x)-1):
                         try:
                              px = position_x[i-1] + (velocity_x[i] + velocity_x[i-1])*math.pow(2*dt,-1)
                              position_x.append(px)
                         except:
                              print("Un available cal") 
         def y_accel_data(dt):
               if len(accel_y) >=2:
                  for i in range(0,len(accel_y)-1):
                       try:
                            vy = velocity_y[i-1] + (accel_y[i] + accel_y[i-1])*math.pow(2*dt,-1)
                            velocity_y.append(vy) 
                       except:
                            print("Un available cal")   
                  for i in range(0,len(accel_y)-1):
                       try:
                            py = position_y[i-1] + (velocity_y[i] + velocity_y[i-1])*math.pow(2*dt,-1)
                            position_y.append(py)
                       except: 
                            print("Un available cal") 
         def z_accel_data(dt):
               if len(accel_z) >=2: 
                  for i in range(0,len(accel_y)-1):
                       try:
                            vz = velocity_z[i-1] + (accel_z[i] + accel_z[i-1])*math.pow(2*dt,-1)
                            velocity_z.append(vz) 
                       except:
                           print("Un available cal")    
                  for i in range(0,len(accel_z)-1):
                       try: 
                            pz = position_z[i-1] + (velocity_z[i] + velocity_z[i-1])*math.pow(2*dt,-1)
                            position_z.append(pz)   
                       except:
                            print("Un available cal")
         x_accel_data(dt)
         y_accel_data(dt)
         z_accel_data(dt)
for i in count(0):
   #print("gyroscope_xout: ", ("%5d" % gyroskop_xout), " skaliert: ", (gyroskop_xout / 131))
   #print("gyroscope_yout: ", ("%5d" % gyroskop_yout), " skaliert: ", (gyroskop_yout / 131))
   #print("gyroscope_zout: ", ("%5d" % gyroskop_zout), " skaliert: ", (gyroskop_zout / 131))
   start_time = time.time() # get the start time

   print("Robot Gyroscope")
   print("---------------------")
 
   beschleunigung_xout = read_word_2c(0x3b)
   beschleunigung_yout = read_word_2c(0x3d)
   beschleunigung_zout = read_word_2c(0x3f)
   accel_data = sensor.get_accel_data()
   gyro_data = sensor.get_gyro_data()
   # Calculate the change in time since the last reading
   current_time = time.time()
   dt = current_time - last_time
   last_time = current_time

   # Calculate the change in rotation along all three axes based on the gyroscope data
   dx = gyro_data['x'] * dt
   dy = gyro_data['y'] * dt
   dz = gyro_data['z'] * dt
   Distance_calculation(dt)
   # Add the change in rotation to the current rotation along all three axes
   x_angle += dx
   y_angle += dy
   z_angle += dz

   beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
   beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
   beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
   AngleDegX = math.degrees(beschleunigung_xout_skaliert)
   AngleDegY = math.degrees(beschleunigung_yout_skaliert)
   AngleDegZ = math.degrees(beschleunigung_zout_skaliert)
   print("AngleDegX",(AngleDegX))
   print("AngleDegY",(AngleDegY))
   print("AngleDegZ",(AngleDegZ))
   print('Acceleration: x={:.2f}g, y={:.2f}g, z={:.2f}g'.format(
        accel_data['x'], accel_data['y'], accel_data['z'])) 
   print('Angles: x={:.2f}deg, y={:.2f}deg, z={:.2f}deg'.format(
        x_angle, y_angle, z_angle))
   Angle_x_dat.append(AngleDegX)
   Angle_y_dat.append(AngleDegY)
   Angle_z_dat.append(dz)
   Accel_x_dat.append(accel_data['x'])
   Accel_y_dat.append(accel_data['y'])
   Accel_z_dat.append(accel_data['z']) 
   if len(Angle_x_dat) > 100:
            Angle_x_dat.remove(Angle_x_dat[0]) 
            Angle_y_dat.remove(Angle_y_dat[0]) 
            Angle_z_dat.remove(Angle_z_dat[0])    
            Accel_x_dat.remove(Accel_x_dat[0])
            Accel_y_dat.remove(Accel_y_dat[0]) 
            Accel_z_dat.remove(Accel_z_dat[0])
   data_trans = {"AngleDegX":Angle_x_dat,"AngleDegY":Angle_y_dat,"AngleDegZ":Angle_z_dat,"Accel_X":Accel_x_dat,"Accel_Y":Accel_y_dat,"Accel_Z":Accel_z_dat,"dx":position_x[len(position_x)-1]*10,"dy":position_x[len(position_x)-1]*10,"dz":position_z[len(position_z)-1]/5}
   print(data_trans)
   
   accel_x.append(data_trans.get("Accel_X")) 
   accel_y.append(data_trans.get("Accel_Y")) 
   accel_z.append(data_trans.get("Accel_Z"))
   if len(accel_x) > 10:
             accel_x.remove(accel_x[0])
             accel_y.remove(accel_y[0]) 
             accel_z.remove(accel_z[0]) 

   #Distance_calculation(dt)
   print("Accel_x",accel_x[len(accel_x)-1],velocity_x[len(velocity_x)-1],position_x[len(position_x)-1],dt)
   print("Accel_y",accel_y[len(accel_y)-1],velocity_y[len(velocity_z)-1],position_y[len(position_y)-1],dt)
   print("Accel_z",accel_z[len(accel_z)-1],velocity_z[len(velocity_z)-1],position_z[len(position_z)-1],dt)   
   #print(position_x[len(position_x)-1],position_y[len(position_y)-1],position_z[len(position_z)-1])
   #Calculate the data of distance and velocity from the acceleration of each axis of the gyroscope 
   
   package_data_iot = {"kornbot380@hotmail.com":{"Motion_sensor":data_trans}}
   #end_time = time.time() # get the end time after end reading the sensor data 
    
   try:
     #res_imu_data = requests.post("https://roboreactor.com/iot_data",json=package_data_iot)
     #res_imu_data = requests.post("http://192.168.50.192:5899/sensor_request",json=package_data_iot)
     res_imu_data = requests.post("https://roboreactor.com/sensor_request",json=package_data_iot)
   except:
      print("Error post request data to the server") 
   
   #print("beschleunigung_xout: ", ("%6d" % beschleunigung_xout), " skaliert: ", beschleunigung_xout_skaliert)
   #print("beschleunigung_yout: ", ("%6d" % beschleunigung_yout), " skaliert: ", beschleunigung_yout_skaliert)
   #print("beschleunigung_zout: ", ("%6d" % beschleunigung_zout), " skaliert: ", beschleunigung_zout_skaliert)
   #print("X Rotation: " , get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))
   #print("Y Rotation: " , get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))
   #time.sleep(0.2)
