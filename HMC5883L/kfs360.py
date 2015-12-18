# Kalman Filter Simple 360 - Simple filter for 360 degrees values
class KFS360:
	X0 = 0.0
	P0 = 0.0
	Q = 0.0
	R = 0.0
	F = 0.0
	H = 0.0
	State = 0.0
	Covariance = 0.0

	def __init__(self, q, r, f, h):
		self.Q = q
		self.R = r
		self.F = f
		self.H = h

	def correct(self, data):
		# +180 -> -180  or -180 -> +180
		if (data > 90 and self.State < -90) or (data < -90 and self.State > 90):
			if data > 0:
				self.State = self.State + 360
			if data < -0:
				self.State = self.State - 360

		self.X0 = self.F*self.State
		self.P0 = self.F*self.Covariance*self.F + self.Q
		K = self.H*self.P0/(self.H*self.P0*self.H + self.R)
		self.State = self.X0 + K*(data - self.H*self.X0)
		self.Covariance = (1 - K*self.H)*self.P0

		if self.State > 180:
			self.State = self.State - 360
		if self.State < -180:
			self.State = self.State + 360

