import numpy as np 
import pickle 
import itertools

def cal_mag(state):
    '''
    Calculate the magnetization of a given bitstring state 
    Args: 
        state (bitstring): sampled bitstring 
    Returns: 
        mag (float): magnetization
    '''
    m = 0
    for a in state:
        if a =='0':
            m += -1
        elif a =="1":
            m += 1
    mag = abs(m)/len(state)
    return mag

def get_mag_dis(unique_mag, pos, bitstrings, spin ):
    '''
    Calculate the distribution of magnetization of different bitstrings
    Args: 
        unique_mag (list): unique magnetization. i.e. [0. 0.5, 0.75, 1]
        pos (list): the position index of bitstrings with the same magnetization in unique mag
        bitstrings (dictionary): sampled results
        spin (int): size of system  
    Returns: 
        mag (float): magnetization
    '''
    shots = 8192 # used in the project
    bitstring_distribution = np.zeros(shape=(2**spin))
    mag_distribution = np.zeros(shape=(len(unique_mag)))
    for i in bitstrings.keys(): 
        bitstring_distribution[int(i,2)]=bitstrings[i]
        mag_distribution[pos[int(i,2)]]+=bitstring_distribution[int(i,2)]
    return mag_distribution/shots

def get_Mag_info(dictory, spin):
    '''
    Getting the information of total magnetization, residual of the magnetization and the 
    norm-2 of the distribution of magnetization compared to the one at the final time
    Args: 
        unique_mag (list): unique magnetization. i.e. [0. 0.5, 0.75, 1]
        pos (list): the position index of bitstrings with the same magnetization in unique mag
        bitstrings (dictionary): sampled results
        spin (int): size of system  
    Returns: 
        mag (float): magnetization
    '''
    mag_list = [cal_mag(np.binary_repr(i,spin)) for i in range(2**spin)]
    unique_mag = list(set(mag_list))
    unique_mag.sort()
    pos=[]
    for i in mag_list: 
        for index,j in enumerate(unique_mag):
            if i == j: 
                pos.append(index)

    Mag, Mag_res, State_res =[], [], []
    for i in np.round(np.arange(1.0, 3.4, 0.1),1):
        runs_mag, runs_state_res, runs_mag_res=[], [], []
        with open(dictory+str(i)+"/"+str(spin)+"@"+str(i)+"w_512", "rb") as f: 
            result = pickle.load(f)
        ref_mag = result[-1]
        ref_sym_dist = get_mag_dis(unique_mag,pos,result[1],spin)
        for j in np.arange(8,512,16):
            with open(dictory+str(i)+"/"+str(spin)+"@"+str(i)+"w"+str(j), "rb") as f: 
                result = pickle.load(f)
            result_sym_dist = get_mag_dis(unique_mag,pos,result[1],spin)
            runs_mag_res.append(np.abs(ref_mag-result[-1]))
            runs_mag.append(result[-1])
            runs_state_res.append(np.linalg.norm(ref_sym_dist-result_sym_dist))
        Mag.append(runs_mag), Mag_res.append(runs_mag_res), State_res.append(runs_state_res)
    return [Mag, Mag_res, State_res ]


def cal_mag_pm_1(spinchain): 
    '''
    Calculate the magnetization with the state composed of 1 and -1, instead of 1 and 0 
    Args: 
        spinchain (list/array): spin configuration
    Returns: 
        mag (float): magnetization
    '''
    return np.abs(np.sum(spinchain))

def my_energy_site(spinchain):
    '''
    Calculate the energy based on the Ising interaction and PBC is applied 
     Args: 
        spinchain (list/array): spin configuration
    Returns: 
        energy (float): energy of the spinchain
    '''
    spins = spinchain.shape[0]
    energy = 0
    for i in range(spins-1):
        energy += spinchain[i]*spinchain[i+1]
    energy += spinchain[0]*spinchain[-1]
    return -energy 

def get_info_1D(spin):
    '''
    Get the information of 1D spin chain, including possible configuration, energy, and magnetization.
    Args: 
        spinchain (list/array): spin configuration
    Returns: 
        information (list): possible_state, energy, mag 
    '''
    elements = [1, -1]
    combinations = list(itertools.product(elements, repeat=spin))
    possible_state = []
    for combination in combinations:
        possible_state.append(np.array(combination))
    energy=[]
    for chain in possible_state: 
        energy.append(my_energy_site(chain))
    mag = np.array([cal_mag_pm_1(state/spin) for state in possible_state])
    return possible_state, energy, mag 


##### 2D #### 
def neighbor_list_2D(i,N): 
    '''
    list the cordination of the for neighboring site based on NxN squre 
    Args: 
        i (list/array): position of the site
        N (int): side length of the square lattice 
    Returns: 
        position (list)
    '''
    row, column = i//N,  i%N
    if row-1 <0: 
        up = (row-1+N)*N+column 
    else: 
        up = (row-1)*N+column
    if row+1 == N: 
        down = column 
    else: 
        down = (row+1)*N+column
    if column-1 < 0: 
        left = row*N+N-1
    else: 
        left = row*N+column-1
    if column+1 == N: 
        right = row*N
    else: 
        right = row*N+column+1
    return [up, down, left, right]

def energy_2D(chain):
    '''
    Calculate the energy based on the 2D Ising interaction and PBC is applied 
     Args: 
        spinchain (list/array): spin configuration
    Returns: 
        energy (float): energy of the spinchain
    '''
    N = int(np.sqrt(len(chain)))
    energy = 0
    for i in range(len(chain)): 
        neighbor = neighbor_list_2D(i,N)
        energy += np.sum([chain[j]*chain[i]/2 for j in neighbor])
    return -energy

def get_info_2D(spin):
    '''
    Get the information of 2D spin lattice, including possible configuration, energy, and magnetization.
    Args: 
        spinchain (list/array): spin configuration
    Returns: 
        information (list): possible_state, energy, mag 
    '''
    elements = [1, -1]
    combinations = list(itertools.product(elements, repeat=spin))
    possible_state = []
    for combination in combinations:
        possible_state.append(np.array(combination))
    energy=[]
    for chain in possible_state: 
        energy.append(energy_2D(chain))
    mag = np.array([cal_mag_pm_1(state/spin) for state in possible_state])
    return possible_state, energy, mag 


def Ry_matrix(theta):   
    '''
    Matrix form of Ry rotation gate 
    Args: 
        theta (float): rotation angle for Ry gate 
    Returns: 
        Ry matrix (array)
    '''

    return np.array([[np.cos(theta/2), -np.sin(theta/2)],
                    [np.sin(theta/2), np.cos(theta/2)]])

def cal_field_energy(angle):
    '''
    Evaluate the energy from the transverse field 
    Args: 
        theta (float): rotation angle for the gate 
    Returns: 
        energy (float)
    '''
    ry = Ry_matrix(angle)
    H_gate = 1/np.sqrt(2)*np.array([[1,1],
                                [1,-1]])
    H_ry = np.dot(H_gate, ry)
    energy = H_ry[0,0]**2 - H_ry[1,0]**2
    return energy