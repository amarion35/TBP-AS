import re
from conllu import parse_tree_incr

class Oracle:
    filename = ''
    regex_conllu = r"\n(\d+)\t([\w\,\.]+\t[\w\,\.]+\t(\w+)\t(\w+)\t([\w\|\=]+)\t(\d+)\t(\w+)\t(\w+)\t([\w\=]+))"
    ref_tree = []

    def __init__(self, filename):
        self.filename = filename
        self.pattern_conllu = re.compile(self.regex_conllu)

    def read_conllu(self):
        with open(self.filename, 'r', encoding='utf8') as file:
            for tokentree in parse_tree_incr(file):
                self.ref_tree.append(tokentree)

    def predict(self):
        pass