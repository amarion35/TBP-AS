import Oracle

class Configuration:
    buffer = []
    pile = []
    arbre = []
    ref_arbre = []

    def __init__(self, filename):
        self.word_list = []
        self.buffer = self.get_words(filename)
        self.oracle = Oracle(filename)
        self.ref_arbre = self.oracle.predict()

    def get_words(self, filename):
        phrases =  ''.join([line for line in open(filename, 'r')]).split('.')
        words = [p.split(' ') for p in phrases]
        return words

    def get_couple(self):
        return self.pile[-1], self.buffer[0]

    def shift(self):
        self.pile.append(self.buffer.pop(0))

    def left(self,type_transition):
        #ajoute arc [mot buffer,type_trans,mot pile] a l abre et supprime mot du dessus de la pile
        arbre.append([self.buffer[0],type_transition,self.pile.pop(-1)])

    def right(self):
        #ajoute arc [mot pile,type_tran,mot buffer] a l arbre et supprime mot dessus de la pile pour l ajouter au debut du buffer
        arbre.append([self.pile[-1],type_transition,self.buffer[0]])
        self.buffer.insert(0,self.pile.pop(-1))
