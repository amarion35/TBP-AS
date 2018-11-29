from Configuration import Configuration
from Oracle import Oracle

filename = "../UD_French-GSD/UD_French-GSD/fr_gsd-ud-train.conllu"

oracle = Oracle(filename)
oracle.search_transitions()

x = oracle.features
y = oracle.transitions