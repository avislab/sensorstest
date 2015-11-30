#!/usr/bin/python

from mpu6050 import *
import time

mpu = MPU6050()
mpu.initialize()

# Set calibration data
mpu.gyro_offs = {'x': -178, 'y': 259, 'z': -104}
mpu.accel_offs =  {'y': -354, 'x': 389, 'z': -1482}

while True:
	accel_data = mpu.get_accel()
	x_rotation = mpu.get_x_rotation(accel_data)
	y_rotation = mpu.get_y_rotation(accel_data)

	print "x:", x_rotation
	print "y:", y_rotation

	time.sleep(0.1)
