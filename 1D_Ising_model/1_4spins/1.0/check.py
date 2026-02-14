import numpy as np 
import pickle
runs = np.arange(8,512,16)
for run in runs: 
    with open('4@1.0w'+str(run), 'rb') as f:
        result = pickle.load(f)
    #with open('4@1.0w512', 'rb') as f: 
     #   ref = pickle.load(f) 
    print(result[0])
