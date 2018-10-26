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
        return self.pile[-1], self.buffer[0]

    def shift(self):
        self.pile.append(self.buffer.pop(0))

    def left(self):
        assert len(self.pile)>1, 'The stack is too short for a left-arc transition'
        assert self.pile[-2]!=root, "You can't make a transition from a word to the root"
        pass

    def right(self):
        assert len(self.pile)>1, 'The stack is too short for a right-arc transition'
        pass