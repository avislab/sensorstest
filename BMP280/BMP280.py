# -*- coding: utf-8 -*-
# Copyright (c) 2015 Andrey Koryagin
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

import smbus
import time

# BMP280 default address.
BMP280_I2CADDR           = 0x77

# BMP280 Registers
BMP280_CONTROL           = 0xF4
BMP280_CONFIG            = 0xF5
BMP280_PRESSURE          = 0xF7
BMP280_TEMP              = 0xFA

BMP280_DIG_T1            = 0x88
BMP280_DIG_T2            = 0x8A
BMP280_DIG_T3            = 0x8C
BMP280_DIG_P1            = 0x8E
BMP280_DIG_P2            = 0x90
BMP280_DIG_P3            = 0x92
BMP280_DIG_P4            = 0x94
BMP280_DIG_P5            = 0x96
BMP280_DIG_P6            = 0x98
BMP280_DIG_P7            = 0x9A
BMP280_DIG_P8            = 0x9C
BMP280_DIG_P9            = 0x9E

# Oversampling Setting
BMP280_OVERS_T1          = 0x20
BMP280_OVERS_T2          = 0x40
BMP280_OVERS_T4          = 0x60
BMP280_OVERS_T8          = 0x80
BMP280_OVERS_T16         = 0xA0

BMP280_OVERS_P1          = 0x04
BMP280_OVERS_P2          = 0x08
BMP280_OVERS_P4          = 0x0C
BMP280_OVERS_P8          = 0x10
BMP280_OVERS_P16         = 0x14

# Power Modes.
# This lib uses NORMAL mode only!
#BMP280_SLEEP_MODE        = 0x00
#BMP280_FORCED_MODE       = 0x01
BMP280_NORMAL_MODE       = 0x03

BMP280_TSB_0_5           = 0x00
BMP280_TSB_62_5          = 0x20
BMP280_TSB_125           = 0x40
BMP280_TSB_250           = 0x60
BMP280_TSB_500           = 0x80
BMP280_TSB_1000          = 0xA0
BMP280_TSB_2000          = 0xC0
BMP280_TSB_4000          = 0xE0

BMP280_FILTER_OFF                = 0x00
BMP280_FILTER_COEFFICIENT2       = 0x04
BMP280_FILTER_COEFFICIENT4       = 0x08
BMP280_FILTER_COEFFICIENT8       = 0x0C
BMP280_FILTER_COEFFICIENT16      = 0x10

BMP280_SPI_OFF           = 0x00
BMP280_SPI_ON            = 0x01

BMP280_CONTROL_SET       = (BMP280_OVERS_T16 | BMP280_OVERS_P16 | BMP280_NORMAL_MODE)
BMP280_CONFIG_SET        = (BMP280_TSB_0_5 | BMP280_FILTER_COEFFICIENT16 | BMP280_SPI_OFF)

class BMP280(object):
	def __init__(self, port=1, address=BMP280_I2CADDR):
		self.bus = smbus.SMBus(port)
		self.address = address

		# Read calibration values
		self.dig_t1 = self.read_word(BMP280_DIG_T1)      # Unsigned
		self.dig_t2 = self.read_word_sign(BMP280_DIG_T2)
		self.dig_t3 = self.read_word_sign(BMP280_DIG_T3)
		self.dig_p1 = self.read_word(BMP280_DIG_P1)      # Unsigned
		self.dig_p2 = self.read_word_sign(BMP280_DIG_P2)
		self.dig_p3 = self.read_word_sign(BMP280_DIG_P3)
		self.dig_p4 = self.read_word_sign(BMP280_DIG_P4)
		self.dig_p5 = self.read_word_sign(BMP280_DIG_P5)
		self.dig_p6 = self.read_word_sign(BMP280_DIG_P6)
		self.dig_p7 = self.read_word_sign(BMP280_DIG_P7)
		self.dig_p8 = self.read_word_sign(BMP280_DIG_P8)
		self.dig_p9 = self.read_word_sign(BMP280_DIG_P9)

		# Set Configuration
                self.write_byte(BMP280_CONFIG, BMP280_CONFIG_SET)
                self.write_byte(BMP280_CONTROL, BMP280_CONTROL_SET)

	def get_data(self):
		adc_t = self.read_long(BMP280_TEMP)
		adc_p = self.read_long(BMP280_PRESSURE)

		var1 = (adc_t/16384.0 - self.dig_t1/1024.0) * self.dig_t2;
		var2 = ((adc_t/131072.0 - self.dig_t1/8192.0) * (adc_t/131072.0 - self.dig_t1/8192.0)) * self.dig_t3;
		t_fine = (var1 + var2);
		temperature = round((t_fine / 5120.0), 2);

		var1 = (t_fine/2.0) - 64000.0;
		var2 = var1 * var1 * self.dig_p6 / 32768.0;
		var2 = var2 + var1 * self.dig_p5 * 2.0;
		var2 = (var2/4.0)+(self.dig_p4 * 65536.0);
		var1 = (self.dig_p3 * var1 * var1 / 524288.0 + self.dig_p2 * var1) / 524288.0;
		var1 = (1.0 + var1 / 32768.0)*self.dig_p1;

		# Avoid exception caused by division by zero
		if (var1 == 0.0):
			return -1

		p = 1048576.0 - adc_p;
		p = (p - (var2 / 4096.0)) * 6250.0 / var1;
		var1 = self.dig_p9 * p * p / 2147483648.0;
		var2 = p * self.dig_p8 / 32768.0;
		pressure = round((p + (var1 + var2 + self.dig_p7) / 16.0), 2);

		return {'t':temperature, 'p':pressure}

	def get_altitude(self, pressure):
		temp = pressure/101325;
		temp = 1-pow(temp, 0.19029);
		altitude = round(44330*temp, 3);
		return altitude;

	def read_byte(self, adr):
		return self.bus.read_byte_data(self.address, adr)

	def read_word(self, adr):
		# ATANTION! Joke from Bosch! LBS before HBS. For calibration registers only!
		lbs = self.bus.read_byte_data(self.address, adr)
		hbs = self.bus.read_byte_data(self.address, adr+1)
		return (hbs << 8) + lbs

	def read_word_sign(self, adr):
		val = self.read_word(adr)
		if (val >= 0x8000):
			return -((65535 - val) + 1)
		else:
			return val

	def read_long(self, adr):
		mbs = self.bus.read_byte_data(self.address, adr)
		lbs = self.bus.read_byte_data(self.address, adr+1)
		xbs = self.bus.read_byte_data(self.address, adr+2)
		val = (mbs << 16) + (lbs << 8) + xbs
		val = (val >> 4)
		return val

	def write_byte(self, adr, byte):
		self.bus.write_byte_data(self.address, adr, byte)
