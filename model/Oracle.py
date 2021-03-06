import re
from Word import Word
from WordBuffer import WordBuffer
import numpy as np

class Oracle:
    mcd =(('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

    def __init__(self, filename):
        self.buffer = WordBuffer(self.mcd)
        self.buffer.readFromConlluFile(filename)
        self.features = []
        self.transitions = []
    
    def search_transitions(self):
        self.features = []
        self.transitions = []
        sentence = self.buffer.nextSentence()
        i = 0
        while sentence:
            i += 1
            root = sentence.pop(0)
            root.setFeat('INDEX', '0')
            pile = [root]
            save_sentence = sentence
            s_features = []
            s_transitions = []
            try:
                while sentence != [root]: # A vérifier
                    last_word_index = eval(sentence[0].getFeat('INDEX'))-1
                    s_features.append([
                        pile[-1].getFeat('POS'),
                        pile[-1].getFeat('LEMMA'),
                        pile[-1].getFeat('MORPHO'),
                        pile[-2].getFeat('POS') if len(pile)>1 else "nan",
                        sentence[0].getFeat('POS'),
                        sentence[0].getFeat('LEMMA'),
                        sentence[0].getFeat('MORPHO'),
                        sentence[1].getFeat('POS') if len(sentence)>1 else "nan",
                        save_sentence[last_word_index].getFeat('POS') if (len(save_sentence)>last_word_index and last_word_index>-1) else "nan",
                        eval(sentence[0].getFeat('INDEX'))-eval(pile[-1].getFeat('INDEX'))
                    ])
                    buffer_word = sentence[0]
                    buffer_index = buffer_word.getFeat('INDEX')
                    pile_word = pile[-1]
                    pile_index = pile_word.getFeat('INDEX')
                    buff_links = [w.getFeat('GOV') for w in sentence[1:]]
                    if pile_index == buffer_word.getFeat('GOV') and buffer_index not in buff_links: # et il ne reste pas d'autres relations avec le mot du buffer
                        t = {'transition': 'right', 'type': buffer_word.getFeat('LABEL')}
                        s_transitions.append(t)
                        sentence.pop(0)
                        sentence.insert(0, pile.pop(-1))
                    elif pile_word.getFeat('GOV') == buffer_index and pile_index not in buff_links:
                        t = {'transition': 'left', 'type': pile_word.getFeat('LABEL')}
                        s_transitions.append(t)
                        pile.pop(-1)
                    else:
                        t = {'transition': 'shift'}
                        s_transitions.append(t)
                        pile.append(buffer_word)
                        sentence.pop(0)
                self.features.append(s_features)
                self.transitions.append(s_transitions)
            except Exception:
                #print('Error abort this sentence')
                pass
            sentence = self.buffer.nextSentence()
        self.features = [self.features[i][j] for i in range(len(self.features)) for j in range(len(self.features[i]))]
        self.transitions = [self.transitions[i][j] for i in range(len(self.transitions)) for j in range(len(self.transitions[i]))]