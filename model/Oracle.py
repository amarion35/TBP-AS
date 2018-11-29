import re
from Word import Word
from WordBuffer import WordBuffer

class Oracle:
    mcd =(('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

    def __init__(self, filename):
        self.buffer = WordBuffer(self.mcd)
        self.buffer.readFromConlluFile(filename)
        self.features = []
        self.transitions = []
    
    def search_transitions(self):
        sentence = self.buffer.nextSentence()
        i = 0
        while sentence:
            i += 1
            print(i)
            root = sentence.pop(0)
            root.setFeat('INDEX', '0')
            pile = [root]
            try:
                while sentence != [root]: # A vérifier
                    buffer_word = sentence[0]
                    buffer_index = buffer_word.getFeat('INDEX')
                    pile_word = pile[-1]
                    pile_index = pile_word.getFeat('INDEX')
                    buff_links = [w.getFeat('GOV') for w in sentence[1:]]
                    if pile_index == buffer_word.getFeat('GOV') and buffer_index not in buff_links: # et il ne reste pas d'autres relations avec le mot du buffer
                        t = {'transition': 'right', 'type': buffer_word.getFeat('LABEL')}
                        self.transitions.append(t)
                        sentence.pop(0)
                        sentence.insert(0, pile.pop(-1))
                    elif pile_word.getFeat('GOV') == buffer_index and pile_index not in buff_links:
                        t = {'transition': 'left', 'type': pile_word.getFeat('LABEL')}
                        self.transitions.append(t)
                        pile.pop(-1)
                    else:
                        t = {'transition': 'shift'}
                        self.transitions.append(t)
                        pile.append(buffer_word)
                        sentence.pop(0)
                    #print(t)
                    #print(pile, sentence)
            except Exception:
                print('Error abort this sentence')
            sentence = self.buffer.nextSentence()
        return self.transitions