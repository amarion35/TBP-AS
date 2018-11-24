from Configuration import Configuration

configuration = Configuration()
oracle = configuration.oracle
oracle.search_transitions()
print(oracle.transitions)

