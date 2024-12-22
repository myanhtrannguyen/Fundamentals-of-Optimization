from ortools.linear_solver import pywraplp

def traveling_salesman_with_ortools(n, distance_matrix):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return "Solver not available"

    # Variables: x[i][j] is 1 if the path goes from city i to city j
    x = [[solver.BoolVar(f'x[{i},{j}]') for j in range(n)] for i in range(n)]

    # Variables: u[i] to eliminate subtours
    u = [solver.IntVar(0, n - 1, f'u[{i}]') for i in range(n)]

    # Objective function: minimize the total distance
    solver.Minimize(solver.Sum(distance_matrix[i][j] * x[i][j] for i in range(n) for j in range(n)))

    # Constraints: each city is visited exactly once
    for i in range(n):
        solver.Add(solver.Sum(x[i][j] for j in range(n) if i != j) == 1)
        solver.Add(solver.Sum(x[j][i] for j in range(n) if i != j) == 1)

    # Subtour elimination constraints (MTZ formulation)
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                solver.Add(u[i] - u[j] + n * x[i][j] <= n - 1)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        return int(solver.Objective().Value())
    else:
        return "NO_SOLUTION"

# Input
n = int(input())
distance_matrix = [list(map(int, input().split())) for _ in range(n)]

# Output
result = traveling_salesman_with_ortools(n, distance_matrix)
print(result)
