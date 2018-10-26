import sys
from WordBuffer import WordBuffer


mcd =(('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

wb = WordBuffer(mcd);
wb.readFromConlluFile("UD_French-GSD/fr_gsd-ud-train.conllu");

#wb.affiche(mcd)
print(len(wb.array))
for i in wb.array[0:10]:
        i.affiche(mcd)


def printSentence(sentence, mcd):
    for i in range(0, len(sentence)):
        sentence[i].affiche(mcd)

"""
sentence = wb.nextSentence()
sentNb = 1
while sentence :
    print('sentence', sentNb)
    printSentence(sentence, mcd)
    sentNb += 1
    sentence = wb.nextSentence()
"""