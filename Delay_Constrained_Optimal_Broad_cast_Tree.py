import sys
from ortools.sat.python import cp_model

def Input():
    [n,m,s,L] = [int(x) for x in sys.stdin.readline().split()]
    A = {}
    E = []
    for v in range(1,n+1):
        A[v] = []
    
    for k in range(m):
        [u,v,t,c] = [int(x) for x in sys.stdin.readline().split()]
        A[u].append([v,t,c])
        A[v].append([u,t,c])
        E.append([u,v,c])

    return n,m,s,A,L,E

n,m,s,A,L,E = Input()
# for v in range(1,n+1):
#     print(A[v])
# print(E)
model = cp_model.CpModel()
obj = model.NewIntVar(0, 100000000, "obj")
x = {}
y = {}

for i in range(1,n+1):
    for[j,t,c] in A[i]:
        x[i,j] = model.NewIntVar(0,1,'x(' + str(i) + "," + str(j) + ')' )
        # print("create variable", x[i,j])

for i in range(1,n+1):
    y[i] = model.NewIntVar(0,L,'y(' + str(i) + ')')

for j in range(1,n+1):
    if j !=s:
        model.Add(sum([x[i,j] for [i,t,c] in A[j]]) == 1)

for i in range(1,n+1):
    for [j,t,c] in A[i]:
        b = model.NewBoolVar(" ")
        model.Add(x[i,j]==1).OnlyEnforceIf(b)
        model.Add(x[i,j]==0).OnlyEnforceIf(b.Not())
        model.Add(y[j] == y[i] + t).OnlyEnforceIf(b)

model.Add(y[s]==0)

# for i in range(1,n+1):
#     model.Add(y[i]<=L)


model.Add(sum([x[i,j]*c + x[j,i]*c for [i,j,c] in E]) == obj)

model.Minimize(obj)

solver = cp_model.CpSolver()
status = solver.Solve(model)
# print(x)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(solver.Value(obj))
else:
    print("NO_SOLUTION")


