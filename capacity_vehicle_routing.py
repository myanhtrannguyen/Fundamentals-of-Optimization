n, k, q = map(int, input().split())
d = list(map(int, input().split()))
c = []
for _ in range(n + 1):
    c.append(list(map(int, input().split())))

# Biến toàn cục
y = [0] * (k + 1)  # Xe tải bắt đầu mỗi lộ trình
x = [0] * (n + 1)  # Thứ tự khách hàng trong lộ trình
visited = [False] * (n + 1)  # Trạng thái đã ghé thăm khách hàng
load = [0] * (k + 1)  # Tải trọng của mỗi xe
f = 0  # Chi phí hiện tại
fs = float('inf')  # Chi phí nhỏ nhất tìm được

def checkY(v, truck):
    if v == 0:  # Quay lại kho
        return True
    if load[truck] + d[v - 1] > q:  # Vượt tải
        return False
    if visited[v]:  # Khách hàng đã được phục vụ
        return False
    return True

def Try_X(truck, position):
    global f, fs

    if position > n:  # Hoàn thành tất cả khách hàng
        f += c[x[position - 1]][0]  # Quay lại kho
        fs = min(fs, f)
        f -= c[x[position - 1]][0]
        return

    for v in range(1, n + 1):
        if not visited[v]:
            x[position] = v
            visited[v] = True
            f += c[x[position - 1]][v]

            Try_X(truck, position + 1)

            f -= c[x[position - 1]][v]
            visited[v] = False

def Try_Y(truck):
    global f, fs

    if truck > k:  # Phân phối xong các xe
        Try_X(1, 1)  # Bắt đầu tìm lộ trình
        return

    for v in range(0, n + 1):  # Xét cả việc không phân khách hàng cho xe
        if checkY(v, truck):
            y[truck] = v
            if v > 0:
                visited[v] = True
                load[truck] += d[v - 1]
                f += c[0][v]

            Try_Y(truck + 1)

            if v > 0:
                f -= c[0][v]
                load[truck] -= d[v - 1]
                visited[v] = False

def solve():
    global fs

    Try_Y(1)
    return fs

# Giải bài toán và in kết quả
result = solve()
print(result if result != float('inf') else -1)

