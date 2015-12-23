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
import math
import time

class hmc5883l:
	HMC5883L_DEFAULT_ADDRESS =	0x1E
	HMC5883L_CONFIGURATION_A =	0
	HMC5883L_CONFIGURATION_B =	1
	HMC5883L_MODE =			2
	HMC5883L_OUTX_MBS =		3
	HMC5883L_OUTX_LSB =		4
	HMC5883L_OUTZ_MBS =		5
	HMC5883L_OUTZ_LSB =		6
	HMC5883L_OUTY_MBS =		7
	HMC5883L_OUTY_LSB =		9
	HMC5883L_STATUS =		10
	HMC5883L_IDENTIFICATION_A =	11
	HMC5883L_IDENTIFICATION_B =	12
	HMC5883L_IDENTIFICATION_B =	13

	HMC5883L_scales = {
		0.88: [0, 0.73],
		1.30: [1, 0.92],
		1.90: [2, 1.22],
		2.50: [3, 1.52],
		4.00: [4, 2.27],
		4.70: [5, 2.56],
		5.60: [6, 3.03],
		8.10: [7, 4.35],
	}

	#### Callibration data ###
	calibration_matrix = [	[1.259098, 0.013830, 0.039295],
				[0.01380, 1.245928, -0.018922],
				[0.039295, -0.018922, 1.360489]]
	bias = [11.16, -43.55, -52.62]
	#################################

	def __init__(self, port=1, address=HMC5883L_DEFAULT_ADDRESS, gauss=1.3):
		self.bus = smbus.SMBus(port)
		self.address = address

		# Set HMC5883L Settings
		(reg, self.scale) = self.HMC5883L_scales[gauss]
		# Please read HMC5883L Datasheet before changing followinf settings
		self.bus.write_byte_data(self.address, self.HMC5883L_CONFIGURATION_A, 0x70) # 8 Average, 15 Hz, normal measurement
		self.bus.write_byte_data(self.address, self.HMC5883L_CONFIGURATION_B, reg << 5) # Scale
		self.bus.write_byte_data(self.address, self.HMC5883L_MODE, 0x00) # Continuous measurement

	def read_byte(self, adr):
		return self.bus.read_byte_data(self.address, adr)

	def read_word(self, adr):
		high = self.bus.read_byte_data(self.address, adr)
		low = self.bus.read_byte_data(self.address, adr+1)
		val = (high << 8) + low
		return val

	def read_word_2c(self, adr):
		val = self.read_word(adr)
		if (val >= 0x8000):
			val = -((65535 - val) + 1)
		if val == -4096: return None
		return val

	def write_byte(self, adr, byte):
		self.bus.write_byte_data(self.address, adr, byte)

	def get_raw(self):
		data = {
			'x': self.read_word_2c(self.HMC5883L_OUTX_MBS),
			'y': self.read_word_2c(self.HMC5883L_OUTY_MBS),
			'z': self.read_word_2c(self.HMC5883L_OUTZ_MBS)
		}
		return data

	def get_calibrated(self):
		data = self.get_raw()
		uncalibrated_values = [data['x'] - self.bias[0], data['y'] - self.bias[1], data['z'] - self.bias[2]]
		calibrated_values = [0,0,0]
		for i in range(0,3):
			for j in range(0,3):
				calibrated_values[i] += self.calibration_matrix[i][j] * uncalibrated_values[j];
		return {'x':calibrated_values[0],
			'y':calibrated_values[1],
			'z':calibrated_values[2]}

	def get_axes(self):
		data = self.get_calibrated()
		data['x'] = data['x']*self.scale
		data['y'] = data['y']*self.scale
		data['z'] = data['z']*self.scale
		return data

#	def get_angles(self):
#		data = self.get_calibrated()
#		result = {'x':0, 'y':0, 'z':0}
#		result['x'] = math.pi/2 + math.atan2(data['z'], data['y'])
#		result['y'] = math.pi/2 + math.atan2(data['z'], data['x'])
#		result['z'] = -math.atan2(data['y'], data['x'])
#		return result

#	def get_angles_degrees(self):
#		data = self.get_angles()
#		result = {'x': math.degrees(data['x']), 'y': math.degrees(data['y']), 'z': math.degrees(data['z'])}
#		return result

	def heading(self, Ax=0, Ay=0):
		data = self.get_calibrated()

		Ax = Ax*math.pi/180
		Ay = Ay*math.pi/180

		Mx = [  [1.0, 0.0, 0.0],
			[0.0, math.cos(Ax), -math.sin(Ax)],
			[0.0, math.sin(Ax),  math.cos(Ax)]]

		My = [  [math.cos(Ay), 0.0, math.sin(Ay)],
			[0.0, 1.0, 0.0],
			[-math.sin(Ay), 0.0,  math.cos(Ay)]]

		# Vector rotation
		values = [data['x'],data['y'],data['z']]
		DATA = [0,0,0]
		for i in range(0,3):
			for j in range(0,3):
				DATA[i] += Mx[i][j] * values[j];

		values = [DATA[0],DATA[1],DATA[2]]
		DATA = [0,0,0]
		for i in range(0,3):
			for j in range(0,3):
				DATA[i] += My[i][j] * values[j];

		radians = -math.atan2(DATA[1], DATA[0])

		# Convert to degrees from radians
		return math.degrees(radians)

	def callibration(self):
		f = open('HMC5883L_calibr.txt', 'w')
		print "###############################################"
		print "Please twirl the HMC5883L around a minute..."
		print "The experimental data will stored to HMC5883L_calibr.txt file"
		print "Please use this file to calculate calibration matrix by Magneto software."
		print "###############################################"
		for num in range(0,1000):
			data = self.get_raw()
			f.write(str(data['x'])+'\t'+str(data['y'])+'\t'+str(data['z'])+'\n')
			time.sleep(0.07)
		f.close()
