#!/usr/bin/python

from mpu6050 import *
import time


mpu = MPU6050()
mpu.initialize()

# Set calibration data
mpu.gyro_offs = {'x': -178, 'y': 259, 'z': -104}
mpu.accel_offs =  {'y': -354, 'x': 389, 'z': -1482}

while True:
	gyro_data = mpu.get_gyro()
	accel_data = mpu.get_accel()

	print "Gyro: ", gyro_data
	print "Accel: ", accel_data
	print "Temperature: ",mpu.get_temp()

	time.sleep(0.1)
