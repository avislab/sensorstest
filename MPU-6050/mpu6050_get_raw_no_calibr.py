#!/usr/bin/python

from mpu6050 import *
import time


mpu = MPU6050()
mpu.initialize()

mpu.gyro_offs = {'x': 0, 'y': 0, 'z': 0}
mpu.accel_offs =  {'y': 0, 'x': 0, 'z': 0}


while True:
	gyro_data = mpu.get_gyro()
	accel_data = mpu.get_accel()

	print "Gyro: ", gyro_data
	print "Accel: ", accel_data
	print "Temperature: ",mpu.get_temp()

	time.sleep(0.1)
