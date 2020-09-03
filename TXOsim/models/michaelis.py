# Python model ODEs from antimony file

import numpy as np

def model(y, t, params):

	S = y[0]
	E = y[1]
	P = y[2]
	ES = y[3]

	k1 = params[0]
	k2 = params[1]
	k3 = params[2]

	derivs = [
	- k1*S*E + k2*ES,
	- k1*S*E + k2*ES + k3*ES,
	+ k3*ES,
	+ k1*S*E - k2*ES - k3*ES]
	return derivs
