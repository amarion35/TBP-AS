import numpy as np
from sklearn.model_selection import train_test_split

from Configuration import Configuration
from Oracle import Oracle
from Model import TBP_AS_model

filename = "../UD_French-GSD/UD_French-GSD/fr_gsd-ud-train.conllu"


if __name__=='__main__':
    oracle = Oracle(filename)
    print('oracle parse transitions...')
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

    vocs = [np.array(list(set(x[:,i]))) for i in range(np.shape(x)[1])]
    
    print('sparse encoding of features...')
    x_new = [[np.argwhere(vocs[j]==x[i,j]) for j,feature in enumerate(features)] for i,features in enumerate(x)]
    x_new = np.squeeze(x_new)

    model = TBP_AS_model(vocs)
    classifier = model.classifier

    X_train, X_test, y_train, y_test = train_test_split(x_new, y, test_size=0.33, random_state=42)

    print('model training...')
    classifier.fit(X_train.T.tolist(), y_train, batch_size=1024, epochs=10, verbose=1, validation_data=(X_test.T.tolist(), y_test))