import numpy as np
import os
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pickle
import argparse

from Configuration import Configuration
from Oracle import Oracle
#from Model import TBP_AS_model

filename = "../UD_French-GSD/UD_French-GSD/fr_gsd-ud-train.conllu"

def train(filename):
    oracle = Oracle(filename)
    print('oracle transitions parsing...')
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

    print('sparse encoding of features...')
    vocs, inverses = zip(*(np.unique(feature, return_inverse=True) for feature in x.T))
    x_new = np.vstack(inverses).T
    x_new = np.squeeze(x_new)

    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(x_new, y)

    pickle.dump(vocs, open("vocs.p", "wb"))
    pickle.dump(clf, open("model.p", "wb"))

def predict(filename):
    print('load model...')
    clf = pickle.load(open("model.p", "rb"))
    vocs = pickle.load(open("vocs.p", "rb"))
    print('load configuration...')
    conf = Configuration(filename)
    print('predict transitions...')
    i=0
    while conf.next_sentence():
        i+=1
        print(i)
        try:
            while not conf.end():
                features = conf.get_features()
                features = np.squeeze([np.argwhere(str(f)==vocs[i]) for i,f in enumerate(features)])
                transition = clf.predict([features])[0]
                if transition[0]==1:
                    conf.shift()
                elif transition[1]==1:
                    conf.right('unknown')
                elif transition[2]==1:
                    conf.left('unknown')
        except:
            pass
    print('save configuration in result.conllu...')
    conf.to_collu('result.conllu')

if __name__=='__main__':
    #train(filename)
    parser = argparse.ArgumentParser(description='TBP-AS classifier')
    parser.add_argument('filename', type=str, nargs='+',
                    help='file')
    parser.add_argument('--train', dest='function', action='store_const',
                        const=train, default=predict,
                        help='train a new model')

    args = parser.parse_args()
    filename = args.filename[0]
    print(filename)
    args.function(filename)
