import Oracle

class Configuration:
    buffer = []
    pile = []
    arbre = []
    ref_arbre = []

    def __init__(self, filename):
        self.buffer = self.get_words(filename)
        self.oracle = Oracle(filename)
        self.ref_arbre = self.oracle.predict()

    def get_words(self, filename):
        pass

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