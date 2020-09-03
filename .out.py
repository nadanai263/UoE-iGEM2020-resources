# Cythonized ODEs from antimony file

import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport exp
from libc.math cimport sqrt
from libc.math cimport pow

@cython.cdivision(True) # Zero-division checking turned off
@cython.boundscheck(False) # Bounds checking turned off for this function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def model(np.ndarray[np.float64_t,ndim=1] y, double t, np.ndarray[np.float64_t,ndim=1] params):

	cdef double S1 = y[0]
	cdef double S2 = y[1]

	cdef double k1 = params[0]

	cdef double derivs[2]

	derivs = [
	-k1*S1,
	k1*S1]
	return derivs
