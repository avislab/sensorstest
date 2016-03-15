#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smbus, math, time

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

	def setPWM(self, channel, on, off):
		self.write_byte(self.PCA9685_LED0_ON_L+4*channel, on & 0xFF)
		self.write_byte(self.PCA9685_LED0_ON_H+4*channel, on >> 8)
		self.write_byte(self.PCA9685_LED0_OFF_L+4*channel, off & 0xFF)
		self.write_byte(self.PCA9685_LED0_OFF_H+4*channel, off >> 8)

	def off(self):
		self.write_byte(self.PCA9685_ALL_LED_ON_L, 0)
		self.write_byte(self.PCA9685_ALL_LED_ON_H, 0)
		self.write_byte(self.PCA9685_ALL_LED_OFF_L, 0)
		self.write_byte(self.PCA9685_ALL_LED_OFF_H, 0)

	def read_byte(self, adr):
		return self.bus.read_byte_data(self.address, adr)

	def write_byte(self, adr, byte):
		self.bus.write_byte_data(self.address, adr, byte)


if __name__ == "__main__":
	LED = PCA9685(0x40, 1000)
	LED.setPWM(1,0,0) # channel 1
	LED.setPWM(2,0,0) # channel 2
	LED.setPWM(3,0,0) # channel 3
	for channel in range(1, 4):
		for pwm_led in range (0, 4096, 20):
			LED.setPWM(channel,0,pwm_led)

                for pwm_led in range (4095, 0, -20):
                        LED.setPWM(channel,0,pwm_led)

		LED.setPWM(channel,0,0)
	LED.off()
