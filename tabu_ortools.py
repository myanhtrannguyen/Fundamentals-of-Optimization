from ortools.linear_solver import pywraplp

def solve_lp_ortools(n, m, C, A, b):
    """Giải bài toán LP bằng OR-Tools."""

    # Khai báo solver
    solver = pywraplp.Solver.CreateSolver('GLOP')  # GLOP là solver tuyến tính

    # Tạo biến
    x = [solver.NumVar(0, solver.infinity(), f'x[{i}]') for i in range(n)]

    # Ràng buộc
    for i in range(m):
        constraint = solver.RowConstraint(0, b[i])  # Ràng buộc <=
        for j in range(n):
            constraint.SetCoefficient(x[j], A[i][j])

    # Hàm mục tiêu
    objective = solver.Objective()
    for j in range(n):
        objective.SetCoefficient(x[j], C[j])
    objective.SetMaximization()

    # Giải bài toán
    status = solver.Solve()

    # In kết quả
    if status == pywraplp.Solver.OPTIMAL:
        print(n)
        solution = [x[i].solution_value() for i in range(n)]
        print(" ".join(map(str, solution)))
        #print("Giá trị tối ưu:", solver.Objective().Value()) # Nếu cần in giá trị hàm mục tiêu
        return solution
    elif status == pywraplp.Solver.INFEASIBLE:
        print("INFEASIBLE")
        return "INFEASIBLE"
    elif status == pywraplp.Solver.UNBOUNDED:
        print("UNBOUNDED")
        return "UNBOUNDED"
    else:
        print("PROBLEM HAS NO SOLUTION")
        return "PROBLEM HAS NO SOLUTION"

# Nhập dữ liệu (giống như trước)
n, m = map(int, input().split())
C = list(map(float, input().split()))
A = []
for _ in range(m):
    A.append(list(map(float, input().split())))
b = list(map(float, input().split()))

# Giải bài toán
result = solve_lp_ortools(n, m, C, A, b)