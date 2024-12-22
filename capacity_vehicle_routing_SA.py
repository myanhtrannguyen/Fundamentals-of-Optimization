import random
import math

# Đọc đầu vào
n, k, q = map(int, input().split())
d = list(map(int, input().split()))
c = []
for _ in range(n + 1):
    c.append(list(map(int, input().split())))

# Hàm tính tổng quãng đường của một nghiệm
def calculate_total_distance(solution):
    total_distance = 0
    for route in solution:
        if not route:
            continue
        distance = c[0][route[0]]  # Từ kho đến khách hàng đầu tiên
        for i in range(1, len(route)):
            distance += c[route[i - 1]][route[i]]
        distance += c[route[-1]][0]  # Từ khách hàng cuối về kho
        total_distance += distance
    return total_distance

# Kiểm tra tính hợp lệ của một nghiệm
def is_valid_solution(solution):
    for route in solution:
        load = sum(d[client - 1] for client in route)
        if load > q:
            return False
    return True

# Tạo một nghiệm ngẫu nhiên
def generate_random_solution():
    clients = list(range(1, n + 1))
    random.shuffle(clients)
    solution = [[] for _ in range(k)]
    for client in clients:
        assigned = False
        for route in solution:
            if sum(d[client - 1] for client in route) + d[client - 1] <= q:
                route.append(client)
                assigned = True
                break
        if not assigned:
            return None  # Không thể tạo nghiệm hợp lệ
    return solution

# Tạo một hàng xóm bằng cách hoán đổi 2 khách hàng giữa các xe tải
def generate_neighbor(solution):
    new_solution = [route[:] for route in solution]
    truck1, truck2 = random.sample(range(k), 2)
    if new_solution[truck1] and new_solution[truck2]:
        i = random.randint(0, len(new_solution[truck1]) - 1)
        j = random.randint(0, len(new_solution[truck2]) - 1)
        new_solution[truck1][i], new_solution[truck2][j] = new_solution[truck2][j], new_solution[truck1][i]
    return new_solution

# Thuật toán SA
def simulated_annealing(initial_temperature, cooling_rate, max_iterations):
    current_solution = generate_random_solution()
    while current_solution is None:
        current_solution = generate_random_solution()
    
    current_distance = calculate_total_distance(current_solution)
    best_solution = current_solution
    best_distance = current_distance
    temperature = initial_temperature

    for _ in range(max_iterations):
        neighbor_solution = generate_neighbor(current_solution)
        if not is_valid_solution(neighbor_solution):
            continue
        
        neighbor_distance = calculate_total_distance(neighbor_solution)
        delta = neighbor_distance - current_distance

        # Quy tắc chấp nhận nghiệm
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current_solution = neighbor_solution
            current_distance = neighbor_distance
        
        # Cập nhật nghiệm tốt nhất
        if current_distance < best_distance:
            best_solution = current_solution
            best_distance = current_distance
        
        # Giảm nhiệt độ
        temperature *= cooling_rate

    return best_solution, best_distance

# Tham số của thuật toán SA
initial_temperature = 1000
cooling_rate = 0.995
max_iterations = 10000

# Giải bài toán
solution, distance = simulated_annealing(initial_temperature, cooling_rate, max_iterations)

# In kết quả
print("Minimal Total Distance:", distance)
print("Routes:")
for route in solution:
    print(" -> ".join(map(str, [0] + route + [0])))
