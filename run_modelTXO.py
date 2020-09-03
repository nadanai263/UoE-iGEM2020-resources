import TXOsim.helpers.sbmlIO as sio
import tellurium as te
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

here = "/app" # Docker image mount point. 
#here = os.getcwd() Use this if running locally.

PATH_TO_MODELS = here+"/TXOsim/models/"
PATH_TO_OUTPUT = here+"/TXOsim/output/" # Path for output data, plots
MODELNAME = "TXO"
MODELPY = "TXO.py"
FILENAME = "TXO.csv" # Filename for output data

# Generate ODEs from antimony file
r = te.loada(PATH_TO_MODELS+MODELNAME)
odes = sio.getODEsFromModel(r)
speciesIds, speciesValues, parameterIds, parameterValues, derivatives = sio.parseODEs(r,odes)
sio.writePython(speciesIds,speciesValues,parameterIds,parameterValues,derivatives,PATH_TO_MODELS,MODELPY)
print(odes)

# Solve ODEs 
from TXOsim.models import TXO
y0 = np.array([float(value) for value in speciesValues])
params = np.array([float(value) for value in parameterValues])
TMAX = 12*60*60 # s
NSTEPS = 100

time = np.linspace(0,TMAX,NSTEPS)
sol = odeint(TXO.model, y0, time, args=(params,)) # Scipy solver

# Plot and save plot
for i in range(sol.shape[1]):
    plt.plot(time,sol[:,i], label=speciesIds[i]);
plt.xlabel('t (s)'); plt.ylabel('concs (nM)'); plt.legend()   
plt.savefig(PATH_TO_OUTPUT+'plot.pdf',transparent=True)
#plt.show() 

# Save data
df = pd.DataFrame(sol)
df.to_csv(PATH_TO_OUTPUT+FILENAME, index=None)