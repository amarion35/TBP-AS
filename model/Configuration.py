#import Oracle
import sys
from WordBuffer import WordBuffer

class Configuration:
    buffer = []
    pile = []
    arbre = []
    ref_arbre = []
    root = ''
    mcd =(('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))

    def __init__(self):
        self.word_list = []
        self.pile = []
        self.buffer = WordBuffer(mcd)
        self.buffer.readFromConlluFile("../UD_French-GSD/UD_French-GSD/fr_gsd-ud-train.conllu")
        #self.oracle = Oracle()
        #self.ref_arbre = self.oracle.predict()
        self.transitions = []

    def oracle(self):
        while self.buffer.nextSentence():
            self.pile = [-1]
            buffer_word = self.buffer.getCurrentWord()
            buffer_index = self.buffer.getCurrentIndex()
            pile_word = self.buffer.getWord(self.pile[-1])
            pile_index = self.pile[-1]

            # TODO fin si buffer vide
            if pile_index == buffer_word.getFeat('GOV'):
                self.transition.append({'transition': 'right', 'type': buffer_word.getFeat('LABEL')})
            elif pile_word.getFeat('GOV') == buffer_index:
                self.transition.append({'transition': 'left', 'type': pile_word.getFeat('LABEL')})
            else:
                self.transition.append({'transition': 'shift'})



    def shift(self):
        self.pile.append(self.buffer.getCurrentIndex())
        self.buffer.currentIndex += 1

    def left(self,type_transition):
        assert len(self.pile)>1, 'The stack is too short for a left-arc transition'
        assert self.buffer.getWord(self.pile[-2])!=self.root, "You can't make a transition from a word to the root"
        #ajoute arc [mot buffer,type_trans,mot pile] a l abre et supprime mot du dessus de la pile
        self.buffer.getCurrentWord().setFeat('type_transition', type_transition)
        self.buffer.getCurrentWord().setFeat('gov', self.buffer.getWord(self.pile.pop(-1)))

    def right(self, type_transition):
        assert len(self.pile)>1, 'The stack is too short for a right-arc transition'
        #ajoute arc [mot pile,type_tran,mot buffer] a l arbre et supprime mot dessus de la pile pour l ajouter au debut du buffer
        pile_index = self.pile.pop(-1)
        self.buffer.getWord(pile_index).setFeat('type_transition', type_transition)
        self.buffer.getWord(pile_index).setFeat('gov', self.buffer.getCurrentWord())