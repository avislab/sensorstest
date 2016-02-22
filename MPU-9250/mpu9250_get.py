#!/usr/bin/python

from mpu9250 import *
import time

mpu = MPU9250()
mpu.initialize()

compas = AK8963()
compas.initialize()

# Set calibration data
mpu.gyro_offs =  {'y': -5, 'x': 158, 'z': -100}
mpu.accel_offs =  {'y': 102, 'x': -34, 'z': -364}

compas.calibration_matrix = [  [1.560948, 0.001838, -0.011552],
                                        [0.001838, 1.521376, 0.047572],
                                        [-0.011552, 0.047572, 1.357251]]
compas.bias = [218.92, 115.072, -121.599]

while True:
	gyro_data = mpu.get_gyro()
	accel_data = mpu.get_accel()
	compas_data = compas.get_calibrated()
	
	print "GYROSCOPE: ", gyro_data
	print "ACCELEROMETER: ", accel_data
	print "TEMPERATURE: ",mpu.get_temp()
	print "MAGNETOMETER: ", compas_data, "\n\n"

	time.sleep(1)
