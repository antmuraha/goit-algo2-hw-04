from collections import deque


def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    """
    Breadth-First Search to find an augmenting path in the residual graph.
    Returns True if there is a path from source to sink in residual graph.
    Also fills parent[] to store the path.

    Args:
        capacity_matrix: 2D list representing the capacity of each edge.
        flow_matrix: 2D list representing the current flow of each edge.
        source: Index of the source node.
        sink: Index of the sink node.
        parent: List to store the path.
    Returns:
        bool: True if there is a path from source to sink, False otherwise.
    """
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            # Check if there is residual capacity in the edge
            if (
                not visited[neighbor]
                and capacity_matrix[current_node][neighbor]
                - flow_matrix[current_node][neighbor]
                > 0
            ):
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False


def edmonds_karp(capacity_matrix, source, sink):
    """
    Implements the Edmonds-Karp algorithm to find the maximum flow from source to sink.

    Args:
        capacity_matrix: 2D list representing the capacity of each edge.
        source: Index of the source node.
        sink: Index of the sink node.
    Returns:
        max_flow: The value of the maximum flow.
    """
    num_nodes = len(capacity_matrix)
    flow_matrix = [
        [0] * num_nodes for _ in range(num_nodes)
    ]  # Initialize flow matrix with zeros
    parent = [-1] * num_nodes
    max_flow = 0

    # While there is an augmenting path, add flow
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Find the minimum residual capacity of the edges along the path found (bottleneck)
        path_flow = float("Inf")
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(
                path_flow,
                capacity_matrix[previous_node][current_node]
                - flow_matrix[previous_node][current_node],
            )
            current_node = previous_node

        # Update flow along the path, considering the reverse flow
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        # Increase the maximum flow
        max_flow += path_flow

    return {"max_flow": max_flow, "flow_matrix": flow_matrix}
