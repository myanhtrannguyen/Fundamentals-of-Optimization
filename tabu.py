def simplex_method(n, m, C, A, b):
    """Giải bài toán Simplex không dùng numpy."""

    # Khởi tạo bảng Simplex
    table = [([0.0] * (n + m + 1)) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            table[i][j] = A[i][j]
        table[i][n + i] = 1.0  # Biến bù
        table[i][n + m] = b[i]
    for j in range(n):
        table[m][j] = -C[j]

    basic_vars = list(range(n, n + m))

    while True:
        # Kiểm tra điều kiện tối ưu
        if all(val >= -1e-9 for val in table[m][:-1]):
            break

        # Chọn biến vào
        entering = 0
        for j in range(1, n + m):
            if table[m][j] < table[m][entering]:
                entering = j

        # Kiểm tra tính không giới hạn
        if all(table[i][entering] <= 0 for i in range(m)):
            return "UNBOUNDED"

        # Chọn biến ra
        leaving = 0
        min_ratio = float('inf')
        for i in range(m):
            if table[i][entering] > 1e-9:
                ratio = table[i][n + m] / table[i][entering]
                if ratio < min_ratio:
                    min_ratio = ratio
                    leaving = i

        # Xoay bảng
        pivot = table[leaving][entering]
        for j in range(n + m + 1):
            table[leaving][j] /= pivot

        for i in range(m + 1):
            if i != leaving:
                factor = table[i][entering]
                for j in range(n + m + 1):
                    table[i][j] -= factor * table[leaving][j]

        basic_vars[leaving] = entering

    # Trích xuất nghiệm
    solution = [0.0] * n
    for i in range(m):
        if basic_vars[i] < n:
            solution[basic_vars[i]] = table[i][n + m]

    return solution

# Nhập dữ liệu
n, m = map(int, input().split())
C = list(map(float, input().split()))
A = []
for _ in range(m):
    A.append(list(map(float, input().split())))
b = list(map(float, input().split()))

# Giải bài toán
result = simplex_method(n, m, C, A, b)

# In kết quả
if result == "UNBOUNDED":
    print("UNBOUNDED")
else:
    print(n)
    print(" ".join(map(str, result)))