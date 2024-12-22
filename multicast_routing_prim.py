#
# Input
n, m, s, L = map(int, input().split())
edges = []
for _ in range(m):
    sublist = tuple(map(int, input().split()))
    edges.append(sublist)

def multicast_routing(n, m, s, L, edges):
    # Build the graph
    graph = {i: [] for i in range(1, n + 1)}
    for u, v, t, c in edges:
        graph[u].append((v, t, c))
        graph[v].append((u, t, c))

    # Initialize variables
    visited = set()
    total_cost = 0
    total_time = {i: float('inf') for i in range(1, n + 1)}
    total_time[s] = 0
    pq = [(0, 0, s)]  # (cost, time, node)

    while pq:
        cost, time, node = pq.pop(0)
        if node in visited:
            continue
        visited.add(node)
        total_cost += cost

        for neighbor, t, c in graph[node]:
            if neighbor not in visited:
                new_time = total_time[node] + t
                if new_time <= L and new_time < total_time[neighbor]:
                    total_time[neighbor] = new_time
                    pq.append((c, new_time, neighbor))
        pq.sort()  # Sort by cost for simplicity

    # Check if all nodes are visited
    if len(visited) != n:
        return "NO_SOLUTION"

    return total_cost

# Output
result = multicast_routing(n, m, s, L, edges)
print(result)
