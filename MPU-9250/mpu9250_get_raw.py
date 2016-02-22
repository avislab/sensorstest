#!/usr/bin/python

from mpu9250 import *
import time

mpu = MPU9250()
mpu.initialize()

compas = AK8963()
compas.initialize()

while True:
	gyro_data = mpu.get_gyro_raw()
	accel_data = mpu.get_accel_raw()
	compad_data = compas.get_raw()

	print "GYROSCOPE: ", gyro_data
	print "ACCELEROMETER: ", accel_data
	print "TEMPERATURE: ",mpu.get_temp()
	print "MAGNETOMETER: ", compad_data, "\n\n"
	time.sleep(1)
