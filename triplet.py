

###############################################################################
# HIPEx Monitoring :: datatype Nlet
# 
# This dataclass define class 'Nlet'
# 
# triplet has three state High, Mid, Low
# It was similar with True and False state of datatype 'bool'
#
# specifically, triplet is defined seperately (case of N=3)
#

class Nlet(object):
    def __init__(self,*t):
        self._spins = list(t)
        self._spins.sort()
    def size(self):
        return len(self._spins)
    def config(self):
        self._up = self._spins.count(True)
        self._down = self._spins.count(False)
        self._N = self._up-self._down
        self._spins.sort()
    def __repr__(self):
        config()
        return self._N
    def updown(self, oper):
        if not type(oper) is bool:
            raise TypeError
        if self._spins.count(oper) == len(self._spins):
            return
        else:
            self._spins.remove(not oper)
            self._spins.append(oper)
            self.config()
    def up(self): #rasing operator 
        self.updown(True)
    def down(self): #lowering operator
        self.updown(False)
    def _typecheck(self, other):
        return type(self) is type(other)
    def _sizecheck(self, other):
        if not self._typecheck(other):
            raise TypeError
        return self.size()==other.size()
    def inversion(self):
        Tc = self._spins.count(True)
        Fc = self._spins.count(False)
        self._spins = [True]*Fc + [False]*Tc
        self.config()
    def opposite(self):
        a = self
        Tc = a._spins.count(True)
        Fc = a._spins.count(False)
        a._spins = [True]*Fc + [False]*Tc
        a.config()
        return a
    #compare methods
    def _cmp(self, other):
        if not self._sizecheck(other):
            print("compare different type of value of Nlet")
            raise TypeError
        if self._N<other._N:
            return -1
        elif self._N>other._N:
            return 1
        elif self._N==other._N:
            return 0
        else:
            raise Exception
    def __eq__(self, other):
        return self._cmp(other)==0
    def __ne__(self, other):
        return not self._cmp(other)==0
    def __lt__(self, other):
        return self._cmp(other)==-1
    def __le__(self, other):
        return self._cmp(other)==-1 or self.__cmp(other)==0
    def __gt__(self, other):
        return self._cmp(other)==1
    def __ge__(self, other):
        return self._cmp(other)==1 or self.__cmp(other)==0
    #represent method
    def __repr__(self):
        return str(self.N) + "/" + str(self.size())
    #opposite process


class triplet(Nlet):
    def __init__(self, *state):
        if len(state)==1:
            if state[0]>0:
                self._spins = [True, True]
            if state[0]==0:
                self._spins = [False, True]
            if state[0]<0:
                self._spins = [False, False]
        elif len(state)==2:
            if not state.count(True)+state.count(False)==2:
                print("Triplet\'s number of spins is 2. don\'t input %d \n or the datatype of state tuple is wrong" %len(state)) 
                raise TypeError
            else:
                self._spins=list(state)
        self.config()
    def __repr__ (self):
        if self._N == 2:
            return 'up'
        if self._N == 0:
            return 'zero'
        if self._N == -2:
            return 'down'

class Triplet:
    Up = triplet(1)
    Mid = triplet(0)
    Down = triplet(-1)

if __name__ == "__main__":
    print(Up>Mid)
    print(Up==Mid)
    print(Up==Up)
