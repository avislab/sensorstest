#!/usr/bin/python

from mpu9250 import *

mpu = MPU9250()
mpu.initialize()

mpu.callibration()

compas = AK8963()
compas.initialize()
compas.callibration()

