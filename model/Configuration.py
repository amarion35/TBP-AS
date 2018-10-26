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
        pass

    def left(self):
        pass

    def right(self):
        pass

    def reduc(self):
        pass