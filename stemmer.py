#Implemented Porter Stemmer that only does Step 1 based on the instructions given.
#In Porter Stemmer, Step1 deals with plurals and past participles

class Stemmer:
    def isCons(self, lett):
        if lett == 'a' or lett == 'e' or lett == 'i' or lett == 'o' or lett == 'u':
            return False
        else:
            return True

    def isconsonant(self, term, i):
        lett = term[i]
        if self.isCons(lett):
            if lett == 'y' and self.isCons(term[i - 1]):
                return False
            else:
                return True
        else:
            return False

    def isVowel(self, term, i):
        return not(self.isconsonant(term, i))

    # *S		-		the stem ends with S (and similarly for the other letts).
    def endsWith(self, stem, lett):
        if stem.endswith(lett):
            return True
        else:
            return False

    # *v*		-		the stem contains a vowel.
    def hasVowel(self, stem):
        for i in stem:
            if not self.isCons(i):
                return True
        return False

    # *d		-		the stem ends with a double consonant (e.g. -TT, -SS).
    def doubleconsonant(self, stem):
        if len(stem) >= 2:
            if self.isconsonant(stem, -1) and self.isconsonant(stem, -2):
                return True
            else:
                return False
        else:
            return False

    def getfm(self, term):
        fm = []
        fmStr = ''
        for i in range(len(term)):
            if self.isconsonant(term, i):
                if i != 0:
                    prev = fm[-1]
                    if prev != 'C':
                        fm.append('C')
                else:
                    fm.append('C')
            else:
                if i != 0:
                    prev = fm[-1]
                    if prev != 'V':
                        fm.append('V')
                else:
                    fm.append('V')
        for j in fm:
            fmStr += j
        return fmStr

    def getM(self, term):
        f = self.getfm(term)
        m = f.count('VC')
        return m

    # *o		-		the stem ends cvc, where the second c is not W, X or Y (e.g. -WIL, -HOP).
    def cvc(self, term):
        if len(term) >= 3:
            f = -3
            s = -2
            t = -1
            third = term[t]
            if self.isconsonant(term, f) and self.isVowel(term, s) and self.isconsonant(term, t):
                if third != 'w' and third != 'x' and third != 'y':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def switch(self, orig, rem, rep):
        res = orig.rfind(rem)
        root = orig[:res]
        switchd = root + rep
        return switchd

    def switchM0(self, orig, rem, rep):
        res = orig.rfind(rem)
        root = orig[:res]
        if self.getM(root) > 0:
            switchd = root + rep
            return switchd
        else:
            return orig

    def switchM1(self, orig, rem, rep):
        res = orig.rfind(rem)
        root = orig[:res]
        if self.getM(root) > 1:
            switchd = root + rep
            return switchd
        else:
            return orig

    def step1a(self, term):
        if term.endswith('sses'):
            term = self.switch(term, 'sses', 'ss')
        elif term.endswith('ies'):
            term = self.switch(term, 'ies', 'i')
        elif term.endswith('ss'):
            term = self.switch(term, 'ss', 'ss')
        elif term.endswith('s'):
            term = self.switch(term, 's', '')
        else:
            pass
        return term

    def step1b(self, term):
        boolflag = False
        if term.endswith('eed'):
            res = term.rfind('eed')
            root = term[:res]
            if self.getM(root) > 0:
                term = root
                term += 'ee'
        elif term.endswith('ed'):
            res = term.rfind('ed')
            root = term[:res]
            if self.hasVowel(root):
                term = root
                boolflag = True
        elif term.endswith('ing'):
            res = term.rfind('ing')
            root = term[:res]
            if self.hasVowel(root):
                term = root
                boolflag = True
        if boolflag:
            if term.endswith('at') or term.endswith('bl') or term.endswith('iz'):
                term += 'e'
            elif self.doubleconsonant(term) and not self.endsWith(term, 'l') and not self.endsWith(term, 's') and not self.endsWith(term, 'z'):
                term = term[:-1]
            elif self.getM(term) == 1 and self.cvc(term):
                term += 'e'
            else:
                pass
        else:
            pass
        return term

    def step1c(self, term):
        if term.endswith('y'):
            res = term.rfind('y')
            root = term[:res]
            if self.hasVowel(root):
                term = root
                term += 'i'
        return term


    def stem(self, term):
        term = self.step1a(term)
        term = self.step1b(term)
        term = self.step1c(term)
        return term

def main1():

    #Stem Testing
    # importing modules
    #
    # from nltk.tokenize import word_tokenize
    # ps = Stemmer()
    #
    # sentence = "talk talks talking and talked cat and cats passes passed and passing"
    # terms = word_tokenize(sentence)
    #
    # for w in terms:
    #     print(w, " : ", ps.stem(w))



if __name__ == '__main__':
    main1()

