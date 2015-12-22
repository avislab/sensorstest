#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO

class hcsr04:
	distance = 0
	error = 0

	def __init__(self, TRIGGER=23, ECHO=24):
		self.GPIO_TRIGGER = TRIGGER
		self.GPIO_ECHO = ECHO

		# Define GPIO
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)  # Trigger
		GPIO.setup(self.GPIO_ECHO, GPIO.IN)      # Echo
		GPIO.output(self.GPIO_TRIGGER, False)

		# Allow module to settle
		#time.sleep(0.5)

	def get_distance(self):
		# Send 10us pulse to trigger
		GPIO.output(self.GPIO_TRIGGER, True)
		time.sleep(0.00001)
		GPIO.output(self.GPIO_TRIGGER, False)

		timeout = 0
		start_time = time.time()
		stop_time = start_time
		while GPIO.input(self.GPIO_ECHO)==0:
			start_time = time.time()
			timeout +=1
			if timeout > 1000:
				break

		timeout = 0
		while GPIO.input(self.GPIO_ECHO)==1:
			stop_time = time.time()
			timeout +=1
			if timeout > 1000:
				break

		# Calculate distance
		distance = round((stop_time-start_time)*17150, 2)

		# Check whether the distance is within range
		if distance >= 2 and distance <= 400:
			self.distance = distance
			self.error = 0
			return distance
		else:
			# Out Of Range (incorrect measurement)
			self.error = -1
			return self.distance

	def __del__(self):
		# Reset GPIO settings
		GPIO.cleanup([self.GPIO_TRIGGER, self.GPIO_ECHO])
