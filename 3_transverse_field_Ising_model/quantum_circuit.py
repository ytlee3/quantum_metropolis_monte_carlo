
from qiskit.circuit.library import  RYGate
from qiskit import QuantumCircuit

def pbc_qc(spin,angle,i, build=True ): 
    '''
    Quantum circuit of single MC sweep for 1D model
    Args: 
        spin (int): number of spins 
        angle (float): encode the information of the energy and temperature for accepting probability 
        i (int): index of randomly chosen qubit  
    Returns: 
        qc (QuantumCircuit)
    '''
    # auxiliary qubit 
    aux1,aux2 = spin, spin+1 
    if build:
        qc = QuantumCircuit(spin+2, 1)
    else: 
        qc = QuantumCircuit(spin+2, spin)
    # flip first
    qc.x(i)
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
    # both same sign => rotate with acceptance probability
    ccry = RYGate(angle).control(2,label=None )
    qc.append(ccry,[aux2,aux1,i])
    qc.reset(-1), qc.reset(-2)
    return qc
    