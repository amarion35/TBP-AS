#import Oracle
import sys
from WordBuffer import WordBuffer
from Word import Word

class Configuration:
    buffer = []
    pile = []
    arbre = []
    ref_arbre = []
    mcd =(('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))
    root = Word.fakeWord(mcd)

    def __init__(self):
        self.word_list = []
        self.pile = []
        self.buffer = WordBuffer(self.mcd)
        self.buffer.readFromConlluFile("../UD_French-GSD/UD_French-GSD/fr_gsd-ud-train.conllu")
        self.transitions = []

    def oracle(self):
        sentence = self.buffer.nextSentence()
        while sentence:
            while sentence != [] and self.pile == [self.root]: # A vérifier
                # TODO fin si buffer vide
                buffer_word = sentence[0]
                buffer_index = buffer_word.getFeat('INDEX')
                pile_word = self.pile[-1]
                pile_index = pile_word.getFeat('INDEX')
                if pile_index == buffer_word.getFeat('GOV'):
                    self.transitions.append({'transition': 'right', 'type': buffer_word.getFeat('LABEL')})
                elif pile_word.getFeat('GOV') == buffer_index:
                    self.transitions.append({'transition': 'left', 'type': pile_word.getFeat('LABEL')})
                else:
                    self.transitions.append({'transition': 'shift'})

            sentence = self.buffer.nextSentence()



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

