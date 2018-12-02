#import Oracle
import sys
from WordBuffer import WordBuffer
from Word import Word
from Oracle import Oracle

class Configuration:
    buffer = []
    pile = []
    arbre = []
    ref_arbre = []
    mcd =(('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))
    root = Word.fakeWord(mcd)

    def __init__(self, filename):
        self.word_list = []
        self.pile = []
        self.buffer = WordBuffer(self.mcd)
        self.buffer.readFromConlluFile(filename)
        self.oracle = Oracle(filename)
        self.transitions = []
        self.next_sentence()
        self.sentence = []

    def next_sentence(self):
        self.sentence = self.buffer.nextSentence()
        if not self.sentence: return False
        self.pile=[self.root]
        for i in range(len(self.sentence)):
            self.buffer.getWord(i).setFeat("LABEL", "_")
            self.buffer.getWord(i).setFeat("GOV", "_")
        return True

    def end(self):
        if self.pile==[]: return True
        else: return False

    def get_features(self):
        return [
            self.pile[-1].getFeat('POS'),
            self.pile[-1].getFeat('LEMMA'),
            self.pile[-1].getFeat('MORPHO'),
            self.pile[-2].getFeat('POS') if len(self.pile)>1 else "nan",
            self.buffer.getCurrentWord().getFeat('POS'),
            self.buffer.getCurrentWord().getFeat('LEMMA'),
            self.buffer.getCurrentWord().getFeat('MORPHO'),
            self.buffer.getWord(self.buffer.getCurrentIndex()+1).getFeat('POS') if int(self.buffer.getCurrentWord().getFeat('EOS'))!=1 else "nan",
            self.buffer.getWord(self.buffer.getCurrentIndex()-1).getFeat('POS') if self.buffer.getCurrentIndex()>0 else "nan",
            eval(self.buffer.getCurrentWord().getFeat('INDEX'))-eval(self.pile[-1].getFeat('INDEX'))
            ]

    def shift(self):
        assert self.buffer.currentIndex<len(self.sentence)
        self.pile.append(self.buffer.getCurrentWord())
        self.buffer.currentIndex += 1

    def left(self,type_transition):
        assert len(self.pile)>1, 'The stack is too short for a left-arc transition'
        #assert self.buffer.getWord(self.pile[-2])!=self.root, "You can't make a transition from a word to the root"
        #ajoute arc [mot buffer,type_trans,mot pile] a l abre et supprime mot du dessus de la pile
        self.buffer.getCurrentWord().setFeat('LABEL', type_transition)
        self.buffer.getCurrentWord().setFeat('GOV', self.pile.pop(-1).getFeat('INDEX'))

    def right(self, type_transition):
        assert len(self.pile)>1, 'The stack is too short for a right-arc transition'
        #ajoute arc [mot pile,type_tran,mot buffer] a l arbre et supprime mot dessus de la pile pour l ajouter au debut du buffer
        pile_index = eval(self.pile.pop(-1).getFeat('INDEX'))
        self.buffer.getWord(pile_index).setFeat('LABEL', type_transition)
        self.buffer.getWord(pile_index).setFeat('GOV', self.buffer.getCurrentWord().getFeat('INDEX'))
        self.buffer.currentIndex += 1

    def to_collu(self, filename):
        self.buffer.to_conllu(filename)