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

import smbus
import math
import time

class MPU9250:
	#Register Map for Gyroscope and Accelerometer
	MPU9250_ADDRESS_AD0_LOW    = 0x68 # address pin low (GND), default for InvenSense evaluation board
	MPU9250_ADDRESS_AD0_HIGH   = 0x69 # address pin high (VCC)
	MPU9250_DEFAULT_ADDRESS    = MPU9250_ADDRESS_AD0_LOW

	MPU9250_SELF_TEST_X_GYRO   = 0x00
	MPU9250_SELF_TEST_Y_GYRO   = 0x01
	MPU9250_SELF_TEST_Z_GYRO   = 0x02

	MPU9250_SELF_TEST_X_ACCEL  = 0x0D
	MPU9250_SELF_TEST_Y_ACCEL  = 0x0E
	MPU9250_SELF_TEST_Z_ACCEL  = 0x0F

	MPU9250_XG_OFFSET_H        = 0x13
	MPU9250_XG_OFFSET_L        = 0x14
	MPU9250_YG_OFFSET_H        = 0x15
	MPU9250_YG_OFFSET_L        = 0x16
	MPU9250_ZG_OFFSET_H        = 0x17
	MPU9250_ZG_OFFSET_L        = 0x18

	MPU9250_SMPLRT_DIV         = 0x19
	MPU9250_CONFIG             = 0x1A
	MPU9250_GYRO_CONFIG        = 0x1B
	MPU9250_ACCEL_CONFIG       = 0x1C
	MPU9250_ACCEL_CONFIG2      = 0x1D

	MPU9250_LP_ACCWL_ODR       = 0x1E
	MPU9250_WOM_THR            = 0x1F

	MPU9250_FIFO_EN            = 0x23
	MPU9250_I2C_MST_CTRL       = 0x24
	MPU9250_I2C_SLV0_ADDR      = 0x25
	MPU9250_I2C_SLV0_REG       = 0x26
	MPU9250_I2C_SLV0_CTRL      = 0x27
	MPU9250_I2C_SLV1_ADDR      = 0x28
	MPU9250_I2C_SLV1_REG       = 0x29
	MPU9250_I2C_SLV1_CTRL      = 0x2A
	MPU9250_I2C_SLV2_ADDR      = 0x2B
	MPU9250_I2C_SLV2_REG       = 0x2C
	MPU9250_I2C_SLV2_CTRL      = 0x2D
	MPU9250_I2C_SLV3_ADDR      = 0x2E
	MPU9250_I2C_SLV3_REG       = 0x2F
	MPU9250_I2C_SLV3_CTRL      = 0x30
	MPU9250_I2C_SLV4_ADDR      = 0x31
	MPU9250_I2C_SLV4_REG       = 0x32
	MPU9250_I2C_SLV4_DO        = 0x33
	MPU9250_I2C_SLV4_CTRL      = 0x34
	MPU9250_I2C_SLV4_DI        = 0x35
	MPU9250_I2C_MST_STATUS     = 0x36
	MPU9250_INT_PIN_CFG        = 0x37
	MPU9250_INT_ENABLE         = 0x38
	MPU9250_DMP_INT_STATUS     = 0x39
	MPU9250_INT_STATUS         = 0x3A

	MPU9250_ACCEL_XOUT_H       = 0x3B
	MPU9250_ACCEL_XOUT_L       = 0x3C
	MPU9250_ACCEL_YOUT_H       = 0x3D
	MPU9250_ACCEL_YOUT_L       = 0x3E
	MPU9250_ACCEL_ZOUT_H       = 0x3F
	MPU9250_ACCEL_ZOUT_L       = 0x40
	MPU9250_TEMP_OUT_H         = 0x41
	MPU9250_TEMP_OUT_L         = 0x42
	MPU9250_GYRO_XOUT_H        = 0x43
	MPU9250_GYRO_XOUT_L        = 0x44
	MPU9250_GYRO_YOUT_H        = 0x45
	MPU9250_GYRO_YOUT_L        = 0x46
	MPU9250_GYRO_ZOUT_H        = 0x47
	MPU9250_GYRO_ZOUT_L        = 0x48

	MPU9250_EXT_SENS_DATA_00   = 0x49
	MPU9250_EXT_SENS_DATA_01   = 0x4A
	MPU9250_EXT_SENS_DATA_02   = 0x4B
	MPU9250_EXT_SENS_DATA_03   = 0x4C
	MPU9250_EXT_SENS_DATA_04   = 0x4D
	MPU9250_EXT_SENS_DATA_05   = 0x4E
	MPU9250_EXT_SENS_DATA_06   = 0x4F
	MPU9250_EXT_SENS_DATA_07   = 0x50
	MPU9250_EXT_SENS_DATA_08   = 0x51
	MPU9250_EXT_SENS_DATA_09   = 0x52
	MPU9250_EXT_SENS_DATA_10   = 0x53
	MPU9250_EXT_SENS_DATA_11   = 0x54
	MPU9250_EXT_SENS_DATA_12   = 0x55
	MPU9250_EXT_SENS_DATA_13   = 0x56
	MPU9250_EXT_SENS_DATA_14   = 0x57
	MPU9250_EXT_SENS_DATA_15   = 0x58
	MPU9250_EXT_SENS_DATA_16   = 0x59
	MPU9250_EXT_SENS_DATA_17   = 0x5A
	MPU9250_EXT_SENS_DATA_18   = 0x5B
	MPU9250_EXT_SENS_DATA_19   = 0x5C
	MPU9250_EXT_SENS_DATA_20   = 0x5D
	MPU9250_EXT_SENS_DATA_21   = 0x5E
	MPU9250_EXT_SENS_DATA_22   = 0x5F
	MPU9250_EXT_SENS_DATA_23   = 0x60

	MPU9250_I2C_SLV0_DO        = 0x63
	MPU9250_I2C_SLV1_DO        = 0x64
	MPU9250_I2C_SLV2_DO        = 0x65
	MPU9250_I2C_SLV3_DO        = 0x66
	MPU9250_I2C_MST_DELAY_CTRL = 0x67
	MPU9250_SIGNAL_PATH_RESET  = 0x68
	MPU9250_MOT_DETECT_CTRL    = 0x69
	MPU9250_USER_CTRL          = 0x6A
	MPU9250_PWR_MGMT_1         = 0x6B
	MPU9250_PWR_MGMT_2         = 0x6C
	MPU9250_FIFO_COUNTH        = 0x72
	MPU9250_FIFO_COUNTL        = 0x73
	MPU9250_FIFO_R_W           = 0x74
	MPU9250_WHO_AM_I           = 0x75

	MPU9250_XA_OFFSET_H        = 0x77
	MPU9250_XA_OFFSET_L        = 0x78
	MPU9250_YA_OFFSET_H        = 0x7A
	MPU9250_YA_OFFSET_L        = 0x7B
	MPU9250_ZA_OFFSET_H        = 0x7D
	MPU9250_ZA_OFFSET_L        = 0x7E

	gyro_offs =  {'y': -5, 'x': 158, 'z': -100}
	accel_offs =  {'y': 0, 'x': 0, 'z': 0}

	# construct a new object with the I2C address of the MPU9250
	def __init__(self, address = MPU9250_DEFAULT_ADDRESS):
		self.bus = smbus.SMBus(1)
		self.address = address

	def initialize(self):
		# Now wake the 9250 up as it starts in sleep mode
		# Sleep mode disable, Temperature sensor enable, CLK - internal 8Mhz
		self.write_byte(self.MPU9250_PWR_MGMT_1, 0)
		## Accel Range +-2g
		#self.write_byte(self.MPU9250_ACCEL_CONFIG, 0)
		#self.accel_scale=16384.0
                ## Accel Range +-4g
                self.write_byte(self.MPU9250_ACCEL_CONFIG, 8)
                self.accel_scale=8192.0
                ## Accel Range +-8g
                #self.write_byte(self.MPU9250_ACCEL_CONFIG, 16)
                #self.accel_scale=4096.0
                ## Accel Range +-16g
                #self.write_byte(self.MPU9250_ACCEL_CONFIG, 24)
                #self.accel_scale=2048.0

		# Filter 
		self.write_byte(self.MPU9250_ACCEL_CONFIG2, 8)

		# Gyro Range +-250 degrees/s
		self.write_byte(self.MPU9250_GYRO_CONFIG, 0)
		self.gyro_scale=131
		## Gyro Range +-500 degrees/s
		#self.write_byte(self.MPU9250_GYRO_CONFIG, 8)
		#self.gro_scale=65.5
		## Gyro Range +-1000 degrees/s
		#self.write_byte(self.MPU9250_GYRO_CONFIG, 16)
		#self.gro_scale=32.8
		## Gyro Range +-2000 degrees/s
		#self.write_byte(self.MPU9250_GYRO_CONFIG, 24)
		#self.gro_scale=16.4

		#DLPF Bandwidth = 10
		self.write_byte(self.MPU9250_CONFIG, 5)

		# Enable Magnitometer (address 0x0c)
		self.write_byte(self.MPU9250_INT_PIN_CFG, 2)

	def get_gyro_raw(self):
		data = {
		'x' : self.read_word_2c(self.MPU9250_GYRO_XOUT_H),
		'y' : self.read_word_2c(self.MPU9250_GYRO_YOUT_H),
		'z' : self.read_word_2c(self.MPU9250_GYRO_ZOUT_H) }
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
		'x' : self.read_word_2c(self.MPU9250_ACCEL_XOUT_H),
		'y' : self.read_word_2c(self.MPU9250_ACCEL_YOUT_H),
		'z' : self.read_word_2c(self.MPU9250_ACCEL_ZOUT_H) }
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
		for num in range(0,5000):
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
		print "Please do not move the MPU-9250 some secconds..."
		print "###############################################"
		time.sleep(5)
		self.gyro_offs = self.get_gyro_offs()
		#print "gyro_offs = ", self.gyro_offs
                print "Please twirl the MPU-9250 around a minute"
		print "###############################################"
		self.accel_offs = self.get_accel_offs()
		print "Done. Please use following calibration values:"
		print "###############################################"
		print "gyro_offs = ", self.gyro_offs
		print "accel_offs = ", self.accel_offs
		print "###############################################"		

	def get_temp_raw(self):
		return self.read_word_2c(self.MPU9250_TEMP_OUT_H)

	def get_temp(self):
		return self.get_temp_raw()/340+21.0

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

class AK8963:
	#Register Map for Magnetometer
	AK8963_DEFAULT_ADDRESS     = 0x0C

	AK8963_WIA                 = 0x00
	AK8963_INFO                = 0x01
	AK8963_ST1                 = 0x02
	AK8963_HXL                 = 0x03
	AK8963_HXH                 = 0x04
	AK8963_HYL                 = 0x05
	AK8963_HYH                 = 0x06
	AK8963_HZL                 = 0x07
	AK8963_HZH                 = 0x08
	AK8963_ST2                 = 0x09
	AK8963_CNTL                = 0x0A
	AK8963_RSV                 = 0x0B
	AK8963_ASTC                = 0x0C
	AK8963_TS1                 = 0x0D
	AK8963_TS2                 = 0x0E
	AK8963_I2CDIS              = 0x0F
	AK8963_ASAX                = 0x10
	AK8963_ASAY                = 0x11
	AK8963_ASAZ                = 0x12

	#### Callibration data ###
	calibration_matrix = [  [1.560948, 0.001838, -0.011552],
				[0.001838, 1.521376, 0.047572],
				[-0.011552, 0.047572, 1.357251]]
	bias = [218.92, 115.072, -121.599]

        #################################

	# construct a new object with the I2C address of the MPU9250
	def __init__(self, address = AK8963_DEFAULT_ADDRESS):
		self.bus = smbus.SMBus(1)
		self.address = address

	def read_byte(self, adr):
		return self.bus.read_byte_data(self.address, adr)

	def read_word(self, adr):
		low = self.read_byte(adr)
		high = self.read_byte(adr+1)
		val = (high << 8) + low
		if (val >= 0x8000):
			return -((65535 - val) + 1)
		else:
			return val

	def write_byte(self, adr, byte):
		self.bus.write_byte_data(self.address, adr, byte)

	def initialize(self):
		# Set Fuse ROM access mode
		self.write_byte(self.AK8963_CNTL, 0x0F)
		# Read Magnetic sensor axis sensitivity adjustment value
		self.ASAX = self.read_byte(self.AK8963_ASAX)
		self.ASAY = self.read_byte(self.AK8963_ASAY)
		self.ASAZ = self.read_byte(self.AK8963_ASAZ)
		# Set power-down mode before the transition to another mode.
		self.write_byte(self.AK8963_CNTL, 0x00)
		# Set Continuous measurement mode 0x12 - 8Hz & 16-bit; 0x16 - 100 Hz & 16-bit
		self.write_byte(self.AK8963_CNTL, 0x12)

	def get_raw(self):
		drdy = self.bus.read_byte_data(self.address, self.AK8963_ST1) & 0x01
		if drdy == 1:
			self.X = self.read_word(self.AK8963_HXL)
			self.X = self.read_word(self.AK8963_HXL)*((self.ASAX-128)/256+1)
			self.Y = self.read_word(self.AK8963_HYL)*((self.ASAY-128)/256+1)
			self.Z = self.read_word(self.AK8963_HZL)*((self.ASAZ-128)/256+1)
			hofl = self.bus.read_byte_data(self.address, self.AK8963_ST2) & 0x08
		return {'x':round(self.X), 'y':round(self.Y), 'z':round(self.Z)}

	def callibration(self):
		f = open('AK8963_calibr.txt', 'w')
		print "###############################################"
		print "Please twirl the AK8963 around a minute..."
		print "The experimental data will stored to AK8963_calibr.txt file"
		print "Please use this file to calculate calibration matrix by Magneto software."
		print "###############################################"
		for num in range(0,500):
			data = self.get_raw()
			f.write(str(data['x'])+'\t'+str(data['y'])+'\t'+str(data['z'])+'\n')
			time.sleep(0.125)
		f.close()

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

	def heading(self, Ay=0, Ax=0):
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

		radians = math.atan2(DATA[0], DATA[1])

		# Convert to degrees from radians
		return math.degrees(radians)
