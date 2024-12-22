# PYTHON
n = int(input())
distance_matrix = []
for _ in range(n):
    row = list(map(int, input().split()))
    distance_matrix.append(row)

def tsp_algorithm(n, distance_matrix):
    cur_city = 0
    total_dis = 0
    visited = [False for _ in range(n)]
    visited[0] = True
    path = [0]

    for _ in range(n - 1):
        nearest_city = -1
        min_dis = float('inf')

        for next_city in range(n):
            if not visited[next_city] and distance_matrix[cur_city][next_city] < min_dis:
                nearest_city = next_city
                min_dis = distance_matrix[cur_city][next_city]

        total_dis += min_dis
        cur_city = nearest_city
        visited[cur_city] = True
        path.append(cur_city)

    total_dis += distance_matrix[cur_city][0]
    path.append(0)
    return path, total_dis

path, total_dis = tsp_algorithm(n, distance_matrix)

print(n)
print(' '.join(str(x + 1) for x in path[:-1]))