# -*- coding: utf-8 -*-
# Copyright (c) 2016 Andrey Koryagin
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import smbus, math, time

SERVO_MIN = 204 # 1us ; 4096 - 20 us ; 50 Hz
SERVO_CENTER = 307
SERVO_MAX = 409 # 2us
SERVO_ZONE = SERVO_MAX - SERVO_MIN

class PCA9685:
	PCA9685_MODE1              = 0x00
	PCA9685_MODE2              = 0x01
	PCA9685_SUBADR1            = 0x02
	PCA9685_SUBADR2            = 0x03
	PCA9685_SUBADR3            = 0x04
	PCA9685_PRESCALE           = 0xFE
	PCA9685_LED0_ON_L          = 0x06
	PCA9685_LED0_ON_H          = 0x07
	PCA9685_LED0_OFF_L         = 0x08
	PCA9685_LED0_OFF_H         = 0x09
	PCA9685_ALL_LED_ON_L       = 0xFA
	PCA9685_ALL_LED_ON_H       = 0xFB
	PCA9685_ALL_LED_OFF_L      = 0xFC
	PCA9685_ALL_LED_OFF_H      = 0xFD

	# Bits
	PCA9685_RESTART            = 0x80
	PCA9685_SLEEP              = 0x10
	PCA9685_ALLCALL            = 0x01
	PCA9685_INVRT              = 0x10
	PCA9685_OUTDRV             = 0x04

	def __init__(self, address=0x40, freq=50):
		self.bus = smbus.SMBus(1)
		self.address = address
		prescale = int(math.floor(25000000.0/4096/freq -0.5))

		self.write_byte(self.PCA9685_MODE2, self.PCA9685_OUTDRV)
		self.write_byte(self.PCA9685_MODE1, self.PCA9685_SLEEP)
		time.sleep(0.005)
		self.write_byte(self.PCA9685_PRESCALE, prescale)
		self.write_byte(self.PCA9685_MODE1, self.PCA9685_ALLCALL | self.PCA9685_RESTART)
		time.sleep(0.005)

		self.servos = []
		for idx in range(16):
			servo = Servo()
			self.servos.append(servo)

	def setPWM(self, channel, on, off):
		self.write_byte(self.PCA9685_LED0_ON_L+4*channel, on & 0xFF)
		self.write_byte(self.PCA9685_LED0_ON_H+4*channel, on >> 8)
		self.write_byte(self.PCA9685_LED0_OFF_L+4*channel, off & 0xFF)
		self.write_byte(self.PCA9685_LED0_OFF_H+4*channel, off >> 8)

	def setServo(self, channel, dutycycle):
		# Reverse
		if self.servos[channel].reverse == True:
			if self.servos[channel].signed == True:
				dutycycle = -dutycycle
			else:
				dutycycle = 100.0-dutycycle

		# Exp
		dutycycle = dutycycle/100.0
		exp_val = dutycycle - (self.servos[channel].exp/100.0)*(dutycycle-dutycycle**3)

		if self.servos[channel].signed == True:
			value = SERVO_CENTER + self.servos[channel].servo_trim + (self.servos[channel].servo_max-self.servos[channel].servo_min)*exp_val/2.0
		else:
			value = self.servos[channel].servo_min + self.servos[channel].servo_trim + (self.servos[channel].servo_max-self.servos[channel].servo_min)*exp_val

		# Check Value limits
		if value < self.servos[channel].servo_min:
			value = self.servos[channel].servo_min
		if value > self.servos[channel].servo_max:
			value = self.servos[channel].servo_max

		value = int(value)

		self.setPWM(channel, 0, value)

	def off(self):
		self.write_byte(self.PCA9685_ALL_LED_ON_L, 0)
		self.write_byte(self.PCA9685_ALL_LED_ON_H, 0)
		self.write_byte(self.PCA9685_ALL_LED_OFF_L, 0)
		self.write_byte(self.PCA9685_ALL_LED_OFF_H, 0)

	def read_byte(self, adr):
		return self.bus.read_byte_data(self.address, adr)

	def write_byte(self, adr, byte):
		self.bus.write_byte_data(self.address, adr, byte)

class Servo:
	signed = False #signed=True -100%...+100%  signed=False 0...100%
	reverse = False # reverse
	min = 100.0 # 80%..120%
	max = 100.0 # 80%..120%
	trim = 0.0  # -50..50
	exp = 0.0   # 0..100%

	servo_min = SERVO_MIN
	servo_max = SERVO_MAX
	servo_trim = 0

	def __init__(self):
		return
 	def set(self, signed, reverse, min, max, trim, exp):
		self.signed = signed
		self.reverse = reverse
		self.max = max
		self.min = min
		self.trim = trim
		self.exp = exp
		# Servo Limits % 120%...80% Default 100%
		self.servo_min = SERVO_MIN + SERVO_ZONE*(100.0-self.min)/100.0
		self.servo_max = SERVO_MAX + SERVO_ZONE*(self.max-100.0)/100.0
		# Servo Trim
		self.servo_trim = (self.servo_max-self.servo_min)*self.trim/100.0

		return
