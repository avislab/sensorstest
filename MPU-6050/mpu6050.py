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

class MPU6050:
	MPU6050_ADDRESS_AD0_LOW       = 0x68 # address pin low (GND), default for InvenSense evaluation board
	MPU6050_ADDRESS_AD0_HIGH      = 0x69 # address pin high (VCC)
	MPU6050_DEFAULT_ADDRESS       = MPU6050_ADDRESS_AD0_LOW

	MPU6050_RA_SELF_TEST_X        = 0x0D
	MPU6050_RA_SELF_TEST_Y        = 0x0E
	MPU6050_RA_SELF_TEST_Z        = 0xF
	MPU6050_RA_SELF_TEST_A        = 0x10
	MPU6050_RA_SMPLRT_DIV         = 0x19
	MPU6050_RA_CONFIG             = 0x1A
	MPU6050_RA_GYRO_CONFIG        = 0x1B
	MPU6050_RA_ACCEL_CONFIG       = 0x1C
	MPU6050_RA_FF_THR             = 0x1D
	MPU6050_RA_FF_DUR             = 0x1E
	MPU6050_RA_MOT_THR            = 0x1F
	MPU6050_RA_FIFO_EN            = 0x23
	MPU6050_RA_I2C_MST_CTRL       = 0x24
	MPU6050_RA_I2C_SLV0_ADDR      = 0x25
	MPU6050_RA_I2C_SLV0_REG       = 0x26
	MPU6050_RA_I2C_SLV0_CTRL      = 0x27
	MPU6050_RA_I2C_SLV1_ADDR      = 0x28
	MPU6050_RA_I2C_SLV1_REG       = 0x29
	MPU6050_RA_I2C_SLV1_CTRL      = 0x2A
	MPU6050_RA_I2C_SLV2_ADDR      = 0x2B
	MPU6050_RA_I2C_SLV2_REG       = 0x2C
	MPU6050_RA_I2C_SLV2_CTRL      = 0x2D
	MPU6050_RA_I2C_SLV3_ADDR      = 0x2E
	MPU6050_RA_I2C_SLV3_REG       = 0x2F
	MPU6050_RA_I2C_SLV3_CTRL      = 0x30
	MPU6050_RA_I2C_SLV4_ADDR      = 0x31
	MPU6050_RA_I2C_SLV4_REG       = 0x32
	MPU6050_RA_I2C_SLV4_DO        = 0x33
	MPU6050_RA_I2C_SLV4_CTRL      = 0x34
	MPU6050_RA_I2C_SLV4_DI        = 0x35
	MPU6050_RA_I2C_MST_STATUS     = 0x36
	MPU6050_RA_INT_PIN_CFG        = 0x37
	MPU6050_RA_INT_ENABLE         = 0x38
	MPU6050_RA_DMP_INT_STATUS     = 0x39
	MPU6050_RA_INT_STATUS         = 0x3A
	MPU6050_RA_ACCEL_XOUT_H       = 0x3B
	MPU6050_RA_ACCEL_XOUT_L       = 0x3C
	MPU6050_RA_ACCEL_YOUT_H       = 0x3D
	MPU6050_RA_ACCEL_YOUT_L       = 0x3E
	MPU6050_RA_ACCEL_ZOUT_H       = 0x3F
	MPU6050_RA_ACCEL_ZOUT_L       = 0x40
	MPU6050_RA_TEMP_OUT_H         = 0x41
	MPU6050_RA_TEMP_OUT_L         = 0x42
	MPU6050_RA_GYRO_XOUT_H        = 0x43
	MPU6050_RA_GYRO_XOUT_L        = 0x44
	MPU6050_RA_GYRO_YOUT_H        = 0x45
	MPU6050_RA_GYRO_YOUT_L        = 0x46
	MPU6050_RA_GYRO_ZOUT_H        = 0x47
	MPU6050_RA_GYRO_ZOUT_L        = 0x48
	MPU6050_RA_EXT_SENS_DATA_00   = 0x49
	MPU6050_RA_EXT_SENS_DATA_01   = 0x4A
	MPU6050_RA_EXT_SENS_DATA_02   = 0x4B
	MPU6050_RA_EXT_SENS_DATA_03   = 0x4C
	MPU6050_RA_EXT_SENS_DATA_04   = 0x4D
	MPU6050_RA_EXT_SENS_DATA_05   = 0x4E
	MPU6050_RA_EXT_SENS_DATA_06   = 0x4F
	MPU6050_RA_EXT_SENS_DATA_07   = 0x50
	MPU6050_RA_EXT_SENS_DATA_08   = 0x51
	MPU6050_RA_EXT_SENS_DATA_09   = 0x52
	MPU6050_RA_EXT_SENS_DATA_10   = 0x53
	MPU6050_RA_EXT_SENS_DATA_11   = 0x54
	MPU6050_RA_EXT_SENS_DATA_12   = 0x55
	MPU6050_RA_EXT_SENS_DATA_13   = 0x56
	MPU6050_RA_EXT_SENS_DATA_14   = 0x57
	MPU6050_RA_EXT_SENS_DATA_15   = 0x58
	MPU6050_RA_EXT_SENS_DATA_16   = 0x59
	MPU6050_RA_EXT_SENS_DATA_17   = 0x5A
	MPU6050_RA_EXT_SENS_DATA_18   = 0x5B
	MPU6050_RA_EXT_SENS_DATA_19   = 0x5C
	MPU6050_RA_EXT_SENS_DATA_20   = 0x5D
	MPU6050_RA_EXT_SENS_DATA_21   = 0x5E
	MPU6050_RA_EXT_SENS_DATA_22   = 0x5F
	MPU6050_RA_EXT_SENS_DATA_23   = 0x60
	MPU6050_RA_MOT_DETECT_STATUS  = 0x61
	MPU6050_RA_I2C_SLV0_DO        = 0x63
	MPU6050_RA_I2C_SLV1_DO        = 0x64
	MPU6050_RA_I2C_SLV2_DO        = 0x65
	MPU6050_RA_I2C_SLV3_DO        = 0x66
	MPU6050_RA_I2C_MST_DELAY_CTRL = 0x67
	MPU6050_RA_SIGNAL_PATH_RESET  = 0x68
	MPU6050_RA_MOT_DETECT_CTRL    = 0x69
	MPU6050_RA_USER_CTRL          = 0x6A
	MPU6050_RA_PWR_MGMT_1         = 0x6B
	MPU6050_RA_PWR_MGMT_2         = 0x6C
	MPU6050_RA_BANK_SEL           = 0x6D
	MPU6050_RA_MEM_START_ADDR     = 0x6E
	MPU6050_RA_MEM_R_W            = 0x6F
	MPU6050_RA_DMP_CFG_1          = 0x70
	MPU6050_RA_DMP_CFG_2          = 0x71
	MPU6050_RA_FIFO_COUNTH        = 0x72
	MPU6050_RA_FIFO_COUNTL        = 0x73
	MPU6050_RA_FIFO_R_W           = 0x74
	MPU6050_RA_WHO_AM_I           = 0x75

	gyro_offs = {'x': 0, 'y': 0, 'z': 0}
	accel_offs =  {'y': 0, 'x': 0, 'z': 0}

	# construct a new object with the I2C address of the MPU6050
	def __init__(self, address = MPU6050_DEFAULT_ADDRESS):
		self.bus = smbus.SMBus(1)
		self.address = address

	def initialize(self):
		# Now wake the 6050 up as it starts in sleep mode
		# Sleep mode disable, Temperature sensor enable, CLK - internal 8Mhz
		self.write_byte(self.MPU6050_RA_PWR_MGMT_1, 0)
		## Accel Range +-2g
		#self.write_byte(self.MPU6050_RA_ACCEL_CONFIG, 0)
		#self.accel_scale=16384.0
                ## Accel Range +-4g
                self.write_byte(self.MPU6050_RA_ACCEL_CONFIG, 8)
                self.accel_scale=8192.0
                ## Accel Range +-8g
                #self.write_byte(self.MPU6050_RA_ACCEL_CONFIG, 16)
                #self.accel_scale=4096.0
                ## Accel Range +-16g
                #self.write_byte(self.MPU6050_RA_ACCEL_CONFIG, 24)
                #self.accel_scale=2048.0

		# Gyro Range +-250 degrees/s
		self.write_byte(self.MPU6050_RA_GYRO_CONFIG, 0)
		self.gyro_scale=131
		## Gyro Range +-500 degrees/s
		#self.write_byte(self.MPU6050_RA_GYRO_CONFIG, 8)
		#self.gro_scale=65.5
		## Gyro Range +-1000 degrees/s
		#self.write_byte(self.MPU6050_RA_GYRO_CONFIG, 16)
		#self.gro_scale=32.8
		## Gyro Range +-2000 degrees/s
		#self.write_byte(self.MPU6050_RA_GYRO_CONFIG, 24)
		#self.gro_scale=16.4

		#DLPF Bandwidth = 10
		self.write_byte(self.MPU6050_RA_CONFIG, 5)

	def get_gyro_raw(self):
		data = {
		'x' : self.read_word_2c(self.MPU6050_RA_GYRO_XOUT_H),
		'y' : self.read_word_2c(self.MPU6050_RA_GYRO_YOUT_H),
		'z' : self.read_word_2c(self.MPU6050_RA_GYRO_ZOUT_H) }
		return data

	def get_gyro(self):
		data = self.get_gyro_raw();
		data['x']=(data['x']-self.gyro_offs['x'])/self.gyro_scale
		data['y']=(data['y']-self.gyro_offs['y'])/self.gyro_scale
		data['z']=(data['z']-self.gyro_offs['z'])/self.gyro_scale
		return data

	def get_gyro_offs(self):
		data_offs = {'x':0, 'y':0, 'z':0}
		for num in range(0,100):
			data = self.get_gyro_raw();
			data_offs['x']+=data['x'];
			data_offs['y']+=data['y'];
			data_offs['z']+=data['z'];
		data_offs['x']/=100;
		data_offs['y']/=100;
		data_offs['z']/=100;
		return data_offs

	def get_accel_raw(self):
		data = {
		'x' : self.read_word_2c(self.MPU6050_RA_ACCEL_XOUT_H),
		'y' : self.read_word_2c(self.MPU6050_RA_ACCEL_YOUT_H),
		'z' : self.read_word_2c(self.MPU6050_RA_ACCEL_ZOUT_H) }
		return data

	def get_accel(self):
		data = self.get_accel_raw();
		data['x']=(data['x']-self.accel_offs['x'])/self.accel_scale
		data['y']=(data['y']-self.accel_offs['y'])/self.accel_scale
		data['z']=(data['z']-self.accel_offs['z'])/self.accel_scale
		return data

	def get_accel_offs(self):
		data_offs_min = self.get_accel_raw();
		data_offs_max = self.get_accel_raw();
		for num in range(0,10000):
			data = self.get_accel_raw()
			data_gyro = self.get_gyro()
			if math.fabs(data_gyro['x']) < 2 and  math.fabs(data_gyro['y']) < 2 and  math.fabs(data_gyro['z']) < 2 :
				if data['x'] > data_offs_max['x']:
					data_offs_max['x'] = data['x']

				if data['y'] > data_offs_max['y']:
					data_offs_max['y'] = data['y']

				if data['z'] > data_offs_max['z']:
					data_offs_max['z'] = data['z']

				if data['x'] < data_offs_min['x']:
					data_offs_min['x'] = data['x']

				if data['y'] < data_offs_min['y']:
					data_offs_min['y'] = data['y']

				if data['z'] < data_offs_min['z']:
					data_offs_min['z'] = data['z']

		data = {
		'x': data_offs_min['x']+(data_offs_max['x']-data_offs_min['x'])/2,
		'y': data_offs_min['y']+(data_offs_max['y']-data_offs_min['y'])/2,
		'z': data_offs_min['z']+(data_offs_max['z']-data_offs_min['z'])/2 }
		return data

	def callibration(self):
		print "###############################################"
		print "Please do not move the MPU-6050 some secconds..."
		print "###############################################"
		time.sleep(5)
		self.gyro_offs = self.get_gyro_offs()
		#print "gyro_offs = ", self.gyro_offs
                print "Please twirl the MPU-6050 around a minute"
		print "###############################################"
		self.accel_offs = self.get_accel_offs()
		print "Done. Please change variables"
		print "\"gyro_offs\" and \"accel_offs\""
		print "to following values in mpu6050.py file:"
		print "###############################################"
		print "gyro_offs = ", self.gyro_offs
		print "accel_offs = ", self.accel_offs
		print "###############################################"		

	def get_temp_raw(self):
		return self.read_word_2c(self.MPU6050_RA_TEMP_OUT_H)

	def get_temp(self):
		return self.get_temp_raw()/340+36.53

	def get_gravity(self):
		data = self.get_accel()
		return math.sqrt(data['x']*data['x']+data['y']*data['y']+data['z']*data['z'])

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
			return -((65535 - val) + 1)
		else:
			return val
	def write_byte(self, adr, byte):
		self.bus.write_byte_data(self.address, adr, byte)

	def dist(self, a,b):
		return math.sqrt((a*a)+(b*b))

	def get_y_rotation(self, data):
		radians = math.atan2(data['x'], self.dist(data['y'],data['z']))
		return -math.degrees(radians)

	def get_x_rotation(self, data):
		if data['z'] > 0:
			radians = math.atan2(data['y'], self.dist(data['x'],data['z']))
			if radians < 0:
				radians = 2*math.pi + radians
		else:
			radians = math.pi - math.atan2(data['y'], self.dist(data['x'],data['z']))
		return math.degrees(radians)

