import numpy as np

from Configuration import Configuration
from Oracle import Oracle
from Model import TBP_AS_model

filename = "../UD_French-GSD/UD_French-GSD/fr_gsd-ud-train.conllu"

oracle = Oracle(filename)
oracle.search_transitions()

x = oracle.features
y = oracle.transitions

model = TBP_AS_model(n_features=np.shape(x)[1])

classifier = model.classifier
classifier.fit(x,y)