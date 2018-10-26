import Oracle

class Configuration:
    buffer = []
    pile = []
    arbre = []
    ref_arbre = []
    root = ''

    def __init__(self, filename):
        self.word_list = []
        self.pile = []
        self.buffer = self.get_words(filename)
        self.oracle = Oracle(filename)
        self.ref_arbre = self.oracle.predict()

    def get_words(self, filename):
        phrases =  ''.join([line for line in open(filename, 'r')]).split('.')
        words = [p.split(' ') for p in phrases]
        return words

    def get_couple(self):
        #a remplacer par une fonction featurize(config(config contient les datas du conllu grace a la fonction du prof),fm)
        #qui renvoi l'entree pour le classifieur 
        return self.pile[-1], self.buffer[0]

    def shift(self):
        self.pile.append(self.buffer.pop(0))

    def left(self,type_transition):
        assert len(self.pile)>1, 'The stack is too short for a left-arc transition'
        assert self.pile[-2]!=self.root, "You can't make a transition from a word to the root"
        #ajoute arc [mot buffer,type_trans,mot pile] a l abre et supprime mot du dessus de la pile
        self.arbre.append([self.buffer[0],type_transition,self.pile.pop(-1)])

    def right(self, type_transition):
        assert len(self.pile)>1, 'The stack is too short for a right-arc transition'
        #ajoute arc [mot pile,type_tran,mot buffer] a l arbre et supprime mot dessus de la pile pour l ajouter au debut du buffer
        self.arbre.append([self.pile[-1],type_transition,self.buffer[0]])
        #self.buffer.insert(0,self.pile.pop(-1))
        self.pile.pop(-1) # Pour moi c'est juste ça
