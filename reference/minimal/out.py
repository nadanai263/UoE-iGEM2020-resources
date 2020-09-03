# Python model ODEs from antimony file

import numpy as np

def model(y, t, params):

	S1 = y[0]
	S2 = y[1]

	k1 = params[0]
	k2 = params[1]

	derivs = [
	- k1*S1 + k2*S2,
	+ k1*S1 - k2*S2]
	return derivs
