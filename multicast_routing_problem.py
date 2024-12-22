#LOI CHUA RA DUNG KET QUA
from ortools.linear_solver import pywraplp
n, m, s, L = map(int, input().split())
edges = []
for _ in range(m):
    sublist = tuple(map(int, input().split()))
    edges.append(sublist)
# print(n)
# print(m)
# print(edges)
# def solve_multicast_routing(n, m, s, L, edges):
#     solver = pywraplp.Solver.CreateSolver("SCIP")
#     if not solver:
#         return "Solver not available"
    
#     # x[u, v] is an array of 0-1 variables, which will be 1 if worker edge is concerned.
#     x = {}
#     for u, v, t, c in edges:
#         x[u, v] = solver.BoolVar(f"x[{u},{v}]")
#         x[v, u] = solver.BoolVar(f"x[{v},{u}]") #Add reverse edge for undirected graph
    
#     # y[v] is the tranmission time from the source s to node v
#     y = {v: solver.NumVar(0, L, f"y[{v}]") for v in range (1, n+1)}
        
#     #Constraint
#     for v in range (1, n+1):
#         if v == s:
#             continue
#         inflow = solver.Sum(x[u, v] for u, _, _, _ in edges if (u, v) in x)
#         solver.Add(inflow == 1) #each node has only one inflow except source node

#     #Tranmission time constraint
#     for u, v, t, c in edges:
#         solver.Add(y[v] >= y[u] + t - (1 - x[u,v]) * L)
    
#     for v in range (1, n+1):
#         if v == s:
#             solver.Add(y[v] == 0) #Time at source is 0
#         else:
#             solver.Add(y[v] <= L) #Ensure time constraint

#     # #Ensure connectivity (spanning trê property)
#     # for u, v, t, c in edges:
#     #     solver.Add(x[u,v] + x[v, u] <= 1) #Avoid double counting edges

#     #Objective function: minimize the total cost 
#     solver.Minimize(solver.Sum(x[u,v] * c for u, v, t, c in edges))

#     #solve the problem
#     status = solver.Solve()
#     if status == pywraplp.Solver.OPTIMAL:
#         total_cost = solver.Objective().Value()
#         return int(total_cost)
#     else: 
#         return "NO_SOLUTION"
def solve_multicast_routing(n, m, s, L, edges):
    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return "NO_SOLUTION"

    # Decision variables
    x = {}  # x[(u, v)] = 1 if edge (u, v) is used, 0 otherwise
    for u, v, t, c in edges:
        x[(u, v)] = solver.BoolVar(f'x_{u}_{v}')

    # y[v] represents the transmission time from the source to node v
    y = {v: solver.NumVar(0, L, f'y_{v}') for v in range(1, n + 1)}

    # Constraints
    # 1. Transmission time from source to any node must not exceed L
    for u, v, t, c in edges:
        solver.Add(y[v] >= y[u] + t - (1 - x[(u, v)]) * L)
        solver.Add(y[u] >= y[v] + t - (1 - x[(u, v)]) * L)

    # 2. Ensure each node except the source has exactly one incoming edge
    for v in range(1, n + 1):
        if v == s:
            continue
        incoming_edges = [x[(u, v)] for u, _, _, _ in edges if (u, v) in x]
        solver.Add(solver.Sum(incoming_edges) == 1)

    # 3. Ensure source node's transmission time is 0
    solver.Add(y[s] == 0)

    # Objective: Minimize total cost
    solver.Minimize(solver.Sum(x[(u, v)] * c for u, v, t, c in edges))

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        total_cost = solver.Objective().Value()
        return int(total_cost)
    else:
        return "NO_SOLUTION"
print(solve_multicast_routing(n, m, s, L, edges))

