from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from random import *
from qiskit import Aer
import numpy as np
from qiskit.circuit.library import  RYGate

#circuit for periodic 1D chain 
def pbc_qc(spin,angle,i): 
    # auxiliary qubit 
    aux1,aux2 = spin, spin+1 
    qc = QuantumCircuit(spin+2, spin)
    # flip first
    qc.x(i)
    # qc.barrier()
    if i == 0: 
        neigh1 = i+1
        neigh2 = aux1-1
    elif i == aux1-1:
        neigh1 = i-1
        neigh2 = 0
    else:
        neigh1 = i-1
        neigh2 = i+1
    # check the sign with neighbor
    qc.cx(i, aux1), qc.cx(neigh1, aux1)
    qc.cx(i, aux2), qc.cx(neigh2, aux2)
    # qc.barrier()
    # both same sign => rotate with acceptance probability
    ccry = RYGate(angle).control(2,label=None )
    qc.append(ccry,[aux2,aux1,i])
    qc.reset(-1), qc.reset(-2)
    return qc

def get_1d_qc(spin,angle):  
    # get all possible circuit
    qc_info=[]
    for i in range(spin):
        qc_info.append(pbc_qc(spin,angle,i))
    return qc_info

def get_MC_circuit(initial_qc, qc_info, spin, runs, pre_pick): 
    Pick = []
    for i in range(runs):
        pick = pre_pick[i]
        circuit = qc_info[pick-1]
        initial_qc.compose(circuit, inplace=True)
        Pick.append(pick)
    return initial_qc, Pick

def cal_mag(state): 
    m = 0
    for a in state:
        if a =='0': 
            m += -1
        elif a =="1": 
            m += 1
    mag = abs(m)/len(state)
    return mag
def Mangetization(final_counts, shots): 
    mag = 0
    for i in final_counts.keys(): 
        mag+= (final_counts[i]/shots)*(cal_mag(i))
    return mag

print('Success')
