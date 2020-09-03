# Python model ODEs from antimony file

import numpy as np

def model(y, t, params):

	D = y[0]
	R = y[1]
	RD = y[2]
	N = y[3]
	RDN = y[4]
	M = y[5]

	k1 = params[0]
	k2 = params[1]
	k3 = params[2]
	k4 = params[3]
	k5 = params[4]
	k6 = params[5]

	derivs = [
	- k1*D*R + k2*RD + k5*RDN,
	- k1*D*R + k2*RD + k5*RDN,
	+ k1*D*R - k2*RD - k3*RD*N + k4*RDN,
	- k3*RD*N + k4*RDN,
	+ k3*RD*N - k4*RDN - k5*RDN,
	+ k5*RDN - k6*M]
	return derivs
