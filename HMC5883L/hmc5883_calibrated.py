#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hmc5883 import *

compass = hmc5883l()

# calibration data
compass.calibration_matrix = [  [1.259098, 0.013830, 0.039295],
			[0.01380, 1.245928, -0.018922],
			[0.039295, -0.018922, 1.360489]]
compass.bias = [11.16, -43.55, -52.62]

while True:
	print compass.get_calibrated()
