class KalmanFilterSimple:
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
		self.X0 = self.F*self.State
		self.P0 = self.F*self.Covariance*self.F + self.Q

		#measurement update - correction
		K = self.H*self.P0/(self.H*self.P0*self.H + self.R);
		self.State = self.X0 + K*(data - self.H*self.X0);
		self.Covariance = (1 - K*self.H)*self.P0;

