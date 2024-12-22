import sys

class Var:
    def __init__(self,D,name):
        self.Domain = D
        self.name = name
    def Remove(self,v):
        # remove value v from the domain
        self.Domain.remove(v)

    def Empty(self):
        return len(self.Domain) == 0
    
class Leq:
    def __init__(self, X, Y, D, name):
        # X <= Y + D
        self.X = X
        self.Y = Y
        self.D = D
        self.name = name + '(' + X.name + ' <= ' + Y.name + ' + ' + str(D) + ')'
        self.vars = [X, Y]

    def print(self):
        print(self.name)
        
    def GetVariables(self):
        return self.vars
    
    def HasVariable(self, x):
        return x == self.X or x == self.Y
    
    def Satisfy(self, vx, vy):
        return vx <= vy + self.D
    
    def GetOtherVariable(self, x):
        if x == self.X:
            return self.Y
        elif x == self.Y:
            return self.X
        else: 
            return None
        
class Propagator:
    def __init__(self):
        self.constraints = []
        self.Q = []
        return
    
    def Add(self, constraint):
        self.constraints.append(constraint)

    def print(self):
        for constraint in self.constraints:
            constraint.print()

    def Contains(self, x, c):
        for [xi,ci] in self.Q:
            if x == xi and c == ci:
                return True
        return False
    def ReviseAC3(self,x,c):
        change = False
        vars = c.GetVariables()
        y = c.GetOtherVariable(x)
        R = []
        for vx in x.Domain:
            found = False
            for vy in y.Domain:
                if x == c.X:
                    if c.Satisfy(vx,vy):
                        found = True
                        break
                elif x == c.Y:
                    if c.Satisfy(vy,vx):
                        found = True
                        break
            if found == False:
                R.append(vx)
                change = True
        for v in R:
            x.Remove(v)
        return change
    def AC3(self):
        self.Q = []
        for c in self.constraints:
            for x in c.GetVariables():
                self.Q.append([x,c])

        while len(self.Q) > 0:
            [x,c] = self.Q.pop(0)
            change = self.ReviseAC3(x,c)
            if change:
                if x.Empty():
                    return False
                for c1 in self.constraints:
                    if c1 != c:
                        if c1.HasVariable(x):
                            y = c1.GetOtherVariable(x)
                            if not self.Contains(y,c1):
                                self.Q.append([y,c1])
        return True
    
[n] = [int(x) for x in sys.stdin.readline().split()]
variables = []
prop = Propagator()

for i in range(n):
    line = [int(x) for x in sys.stdin.readline().split()]
    D = set()
    for j in range(1,len(line)):
        D.add(line[j])
    var = Var(D, 'X(' + str(i+1) + ')') #constructor of Vars
    variables.append(var)

        # print('variables = ', len(variables))
[m] = [int(x) for x in sys.stdin.readline().split()]

for k in range(m):
    [i,j,d] = [int(x) for x in sys.stdin.readline().split()]
    c = Leq(variables[i-1], variables[j-1],d,'Leq(' + str(k+1) + ')')
    prop.Add(c)
# prop.print()
ok = prop.AC3()
if ok == False:
    print('FAIL')
else:
    for x in variables:
        LD = [i for i in x.Domain]
        LD.sort()
        print(len(LD), end = ' ')
        for i in LD:
            print(i, end = ' ')
        print()