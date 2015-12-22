#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hcsr04 import *

sonar = hcsr04(23, 24)

while True:
	print sonar.get_distance(), sonar.error
	time.sleep(0.01)

