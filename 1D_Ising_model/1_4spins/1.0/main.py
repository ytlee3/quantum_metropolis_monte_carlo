from function import *
import pickle
import numpy as np
from qiskit import QuantumCircuit, Aer
from qiskit.compiler import transpile
with open("4@1.0w_512", 'rb') as f:
        result = pickle.load(f)
pre_pick = result[0]
spin = 4
temp = 1.0
runs = np.arange(8,512,16)
for run in runs:
    prob = np.exp(-4/temp)
    angle = 2*np.arccos(np.sqrt(prob))
    qc_info = get_1d_qc(spin,angle)
    ####initial condition - could be random 
    start = QuantumCircuit(spin+2, spin)
    start.x(2), start.x(3)
    #####
    mcqc, pick =get_MC_circuit(start, qc_info, spin, run, pre_pick)
    for i in range(spin):
        mcqc.measure(i,i)
        # mcqc.measure_all()
    sim = Aer.get_backend("statevector_simulator")
    qc = transpile(mcqc,sim)
    shots = 8192
    final_counts = sim.run(qc, shots=shots).result().get_counts()
    mag = Mangetization(final_counts,shots)
    results = [pick, final_counts, mag]
    with open(str(spin)+'@'+str(np.round(temp,1))+'w'+str(run), 'wb') as f:
           pickle.dump(results, f)
    print(temp, mag)
