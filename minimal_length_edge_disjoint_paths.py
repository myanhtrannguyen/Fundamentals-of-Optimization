#PYTHON 
from ortools.linear_solver import pywraplp
n, m = map(int, input().split())
edges = []
for _ in range(m):
    sublist = tuple(map(int, input().split()))
    edges.append(sublist)
# print(n)
# print(m)
# print(edges)
def solve_edge_disjoint_paths(n, m, edges):
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return "Solver not available"
    
    # x[u, v] is an array of 0-1 variables, which will be 1 if worker edge is concerned.
    x = {}
    for u, v, c in edges:
        x[u, v] = solver.BoolVar(f"x[{u},{v}]")
        x[v, u] = solver.BoolVar(f"x[{v},{u}]") #Add reverse edge for undirected graph
    
    #Constraint
    #Flow conservation for two paths
    for node in range(1, n+1):
        inflow = []
        outflow = []
        for u, v, c in edges:
            if v == node:
                inflow.append(x[u, v])
            if u == node:
                outflow.append(x[u, v])
        if node == 1: #source node
            solver.Add(solver.Sum(outflow) - solver.Sum(inflow) == 2)
        elif node == n: #sink node
            solver.Add(solver.Sum(inflow) - solver.Sum(outflow) == 2)
        else: #intermediate nodes
            solver.Add(solver.Sum(inflow) - solver.Sum(outflow) == 0)

        # Edge disjoint set
    for u, v, c in edges:
        solver.Add(x[u,v] + x[v,u] <= 1)

    #Objective function: minimize the total cost of two paths
    solver.Minimize(solver.Sum(x[u,v] * c for u, v, c in edges))

    #solve the problem
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        return int(solver.Objective().Value())
    else: 
        return "NOT_FEASIBLE"
print(solve_edge_disjoint_paths(n,m,edges))