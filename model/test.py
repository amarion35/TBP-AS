import numpy as np
import time
from multiprocessing import Pool

from Configuration import Configuration
from Oracle import Oracle
#from Model import TBP_AS_model

filename = "../UD_French-GSD/UD_French-GSD/fr_gsd-ud-train.conllu"
#filename = "../UD_French-GSD/UD_French-GSD/test.conllu"

oracle = Oracle(filename)
oracle.search_transitions()

x = np.array(oracle.features)
y = np.array(oracle.transitions)

y = np.array([k['transition']for k in y])
#shift:0, right:1, left:2
new_y = []
for i in range(len(y)):
    if y[i]=='shift':
        new_y.append([1,0,0])
    elif y[i]=='right':
        new_y.append([0,1,0])
    elif y[i]=='left':
        new_y.append([0,0,1])
        
y = np.array(new_y)
x.shape, y.shape

x_t = x
x = x_t[:1000]

vocs = [np.array(list(set(x[:,i]))) for i in range(np.shape(x)[1])]

def word2index(data):
    i, features = data
    return [np.argwhere(vocs[j]==x[i,j]) for j,feature in enumerate(features)]

if __name__=="__main__":

    t = time.time()
    with Pool(1) as p:
        x_new = list(p.map(word2index, enumerate(x)))
    print(time.time()-t)