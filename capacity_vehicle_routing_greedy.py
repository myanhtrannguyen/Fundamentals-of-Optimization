n, k, q = map(int, input().split())
d = list(map(int, input().split()))
c = []
for _ in range(n + 1):
    c.append(list(map(int, input().split())))

def greedy_solution():
    visited = [False] * (n + 1)  # Trạng thái đã ghé thăm khách hàng
    total_distance = 0  # Tổng quãng đường
    remaining_load = [q] * k  # Tải trọng còn lại của từng xe
    paths = [[] for i in range (k)]
    for truck in range(k):
        current_location = 0  # Bắt đầu từ kho
        truck_distance = 0  # Quãng đường của xe tải hiện tại

        while True:
            nearest_client = -1
            min_distance = float('inf')

            # Tìm khách hàng gần nhất còn trong tải trọng
            for client in range(1, n + 1):
                if not visited[client] and remaining_load[truck] >= d[client - 1]:
                    if c[current_location][client] < min_distance:
                        min_distance = c[current_location][client]
                        nearest_client = client
                        paths[truck - 1].append(client)

            if nearest_client == -1:  # Không còn khách hàng phù hợp
                break

            # Cập nhật trạng thái khi chọn khách hàng
            visited[nearest_client] = True
            remaining_load[truck] -= d[nearest_client - 1]
            truck_distance += min_distance
            current_location = nearest_client

        # Quay về kho
        truck_distance += c[current_location][0]
        total_distance += truck_distance
    print(paths)
    return total_distance

# In kết quả
result = greedy_solution()
print(result)
