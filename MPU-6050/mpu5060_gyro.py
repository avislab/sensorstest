#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from mpu6050 import *

mpu = MPU6050()
mpu.initialize()

# Set calibration data
mpu.gyro_offs = {'x': -178, 'y': 259, 'z': -104}
mpu.accel_offs =  {'y': -354, 'x': 389, 'z': -1482}

accel_data = mpu.get_accel()
x_rotation = 0
y_rotation = 0
last_time = time.time()

while True:
	new_time = time.time()
	gyro_data = mpu.get_gyro()

	dt = new_time - last_time
	last_time = new_time
	x_rotation = gyro_data['x']*dt + x_rotation

	if x_rotation > 360:
		x_rotation -= 360
	if x_rotation < 0:
		x_rotation = 360 + x_rotation

	y_rotation = gyro_data['y']*dt + y_rotation

        print "x:", x_rotation
        print "y:", y_rotation

	time.sleep(0.01)

