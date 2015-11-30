#!/usr/bin/python

from mpu6050 import *
from kf import *
import time

mpu = MPU6050()
mpu.initialize()

# Set calibration data
mpu.gyro_offs = {'x': -178, 'y': 259, 'z': -104}
mpu.accel_offs =  {'y': -354, 'x': 389, 'z': -1482}

# Simple Kalman Filter
# Q=2; R=15; F=1; H=1
# Q - noise
# R - measuring erro
# F - dynamics of the system
# H - 1
kf_x = KalmanFilterSimple(2.0, 1.0, 1.0, 1.0);
kf_y = KalmanFilterSimple(2.0, 1.0, 1.0, 1.0);

last_time = time.time()

while True:
	new_time = time.time()
	accel_data = mpu.get_accel()

	x_rotation = mpu.get_x_rotation(accel_data)
	y_rotation = mpu.get_y_rotation(accel_data)

	kf_x.correct(x_rotation)
	kf_y.correct(y_rotation)

	print "x:", kf_x.State
	print "y:", kf_y.State

	time.sleep(0.1)
