class Word:

    def __init__(self):
        self.featDic = {}

    def __repr__(self):
        return " *{}".format(self.getFeat('FORM'))
        

    def getFeat(self, featName):
        if(not featName in self.featDic):
            print('WARNING : feat', featName, 'does not exist')
            return None
        else:
            return self.featDic[featName]

    def setFeat(self, featName, featValue):
        self.featDic[featName] = featValue

    def affiche(self, mcd):
        for elt in mcd:
            feat, status = elt
            print(self.getFeat(feat), '\t', end='')
        print('')

        
    @staticmethod
    def fakeWord(mcd):
        w =Word()
        for elt in mcd:
            feat, status = elt
            w.setFeat(feat, 'ROOT')
        w.setFeat('INDEX', '-1')
        return w

    @staticmethod
    def invalidGov():
        return 123456789

    @staticmethod
    def invalidLabel():
        return ''

