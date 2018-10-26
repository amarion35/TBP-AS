from Oracle import Oracle

filename = r"..\UD_French-GSD\UD_French-GSD\fr_gsd-ud-dev.conllu"

oracle = Oracle(filename)
oracle.read_conllu()