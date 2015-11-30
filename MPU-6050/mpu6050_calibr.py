#!/usr/bin/python

from mpu6050 import *
from kf import *
import time

mpu = MPU6050()
mpu.initialize()
mpu.callibration()
