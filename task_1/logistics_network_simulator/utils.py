import networkx as nx


def prepare_capacity_matrix(G):
    """
    Prepares the capacity matrix from the graph.
    """
    capacity_matrix = nx.to_numpy_array(G, weight="capacity")
    return capacity_matrix


def check_optimal_flow(G, source, sink, max_flow):
    """
    Checks if the optimal flow has been achieved and explains why.

    Args:
        G: NetworkX DiGraph
        source: Source node name
        sink: Sink node name
        max_flow: The calculated maximum flow value

    Returns:
        dict: Analysis results including whether flow is optimal and explanation
    """
    # Calculate total capacity from source
    source_capacity = sum(
        G[source][neighbor]["capacity"] for neighbor in G.successors(source)
    )

    # Calculate total capacity to sink
    sink_capacity = sum(
        G[predecessor][sink]["capacity"] for predecessor in G.predecessors(sink)
    )

    # Find the minimum cut using NetworkX
    cut_value, partition = nx.minimum_cut(G, source, sink, capacity="capacity")

    # Check if flow saturates source or sink
    source_saturated = max_flow >= source_capacity
    sink_saturated = max_flow >= sink_capacity

    # Optimal flow is achieved when:
    # 1. Max flow equals the minimum cut value (by max-flow min-cut theorem)
    # 2. No augmenting path exists (already guaranteed by the algorithm)
    is_optimal = (
        abs(max_flow - cut_value) < 1e-9
    )  # Using small epsilon for floating point comparison

    analysis = {
        "max_flow": max_flow,
        "min_cut_value": cut_value,
        "source_capacity": source_capacity,
        "sink_capacity": sink_capacity,
        "is_optimal": is_optimal,
        "source_saturated": source_saturated,
        "sink_saturated": sink_saturated,
        "bottleneck": min(source_capacity, sink_capacity, cut_value),
    }

    # Generate explanation
    explanation = []
    explanation.append(f"\n{'=' * 70}")
    explanation.append("OPTIMAL FLOW ANALYSIS")
    explanation.append(f"{'=' * 70}")
    explanation.append(f"Maximum Flow: {max_flow} units")
    explanation.append(f"Minimum Cut Value: {cut_value} units")
    explanation.append(f"Total Capacity from {source}: {source_capacity} units")
    explanation.append(f"Total Capacity to {sink}: {sink_capacity} units")
    explanation.append(f"{'-' * 70}")

    if is_optimal:
        """
        The flow is optimal because the value of the maximum flow equals the capacity of the minimum cut.
        No augmenting path exists from SUPER_SOURCE to SUPER_SINK in the residual graph, therefore the flow cannot be increased.
        """
        explanation.append("✓ OPTIMAL FLOW ACHIEVED!")
        explanation.append(
            f"The flow is optimal because the value of the maximum flow equals the capacity of the minimum cut."
        )
        explanation.append(
            f"No augmenting path exists from {source} to {sink} in the residual graph, therefore the flow cannot be increased."
        )
        explanation.append(f"\nBy the Max-Flow Min-Cut Theorem:")
        explanation.append(
            f"  - The maximum flow ({max_flow}) equals the minimum cut ({cut_value})"
        )
        explanation.append(
            f"  - This means no augmenting path exists in the residual graph"
        )
        explanation.append(f"  - The flow cannot be increased further\n")

        if source_saturated:
            explanation.append(f"  - The source '{source}' is fully saturated")
            explanation.append(
                f"    (all {source_capacity} units of outgoing capacity are used)"
            )

        if sink_saturated:
            explanation.append(f"  - The sink '{sink}' is fully saturated")
            explanation.append(
                f"    (all {sink_capacity} units of incoming capacity are used)"
            )

        explanation.append(
            f"\n  The network bottleneck is {analysis['bottleneck']} units."
        )
    else:
        explanation.append("✗ OPTIMAL FLOW NOT ACHIEVED")
        explanation.append(f"  - There is a discrepancy between max flow and min cut")
        explanation.append(f"  - This may indicate an error in the calculation")

    explanation.append(f"{'=' * 70}\n")

    analysis["explanation"] = "\n".join(explanation)

    return analysis


def analyze_network_flow(G, sources, sinks):
    """
    Analyzes the overall network flow for all source-sink pairs.

    Args:
        G: NetworkX DiGraph
        sources: List of source node names
        sinks: List of sink node names

    Returns:
        dict: Comprehensive analysis of the network
    """
    total_analysis = {
        "source_total_capacity": 0,
        "sink_total_capacity": 0,
        "max_possible_flow": 0,
    }

    # Calculate total capacity from all sources
    for source in sources:
        capacity = sum(
            G[source][neighbor]["capacity"] for neighbor in G.successors(source)
        )
        total_analysis["source_total_capacity"] += capacity

    # Calculate total capacity to all sinks
    for sink in sinks:
        capacity = sum(
            G[predecessor][sink]["capacity"] for predecessor in G.predecessors(sink)
        )
        total_analysis["sink_total_capacity"] += capacity

    # The theoretical maximum flow is limited by the minimum of source and sink capacities
    total_analysis["max_possible_flow"] = min(
        total_analysis["source_total_capacity"], total_analysis["sink_total_capacity"]
    )

    print(f"\n{'=' * 70}")
    print("NETWORK CAPACITY ANALYSIS")
    print(f"{'=' * 70}")
    print(
        f"Total capacity from all sources (terminals): {total_analysis['source_total_capacity']} units"
    )
    print(
        f"Total capacity to all sinks (stores): {total_analysis['sink_total_capacity']} units"
    )
    print(
        f"Theoretical maximum possible flow: {total_analysis['max_possible_flow']} units"
    )
    print(f"{'=' * 70}\n")

    return total_analysis


def create_unified_network(G, sources, sinks):
    """
    Creates a network with super source and super sink for overall analysis.
    This enables analysis of the ENTIRE network as a single system.

    Args:
        G: Original NetworkX DiGraph
        sources: List of source nodes (terminals)
        sinks: List of sink nodes (stores)

    Returns:
        Modified graph with super source 'SUPER_SOURCE' and super sink 'SUPER_SINK'
    """
    G_unified = G.copy()

    # Add super source connected to all terminals with infinite capacity
    # (since terminals themselves limit the flow)
    for source in sources:
        capacity = sum(
            G[source][neighbor]["capacity"] for neighbor in G.successors(source)
        )
        G_unified.add_edge("SUPER_SOURCE", source, capacity=capacity)

    # Add super sink connected from all stores with infinite capacity
    # (since stores themselves limit the incoming flow)
    for sink in sinks:
        capacity = sum(
            G[predecessor][sink]["capacity"] for predecessor in G.predecessors(sink)
        )
        G_unified.add_edge(sink, "SUPER_SINK", capacity=capacity)

    return G_unified


def calculate_network_max_flow(G, sources, sinks):
    """
    Calculates the maximum flow for the ENTIRE logistics network.
    This treats all terminals and stores as a unified system.

    Args:
        G: NetworkX DiGraph (original network)
        sources: List of source node names (terminals)
        sinks: List of sink node names (stores)

    Returns:
        dict: Contains max flow value, flow distribution, and optimality analysis
    """
    # Create unified network with super source and super sink
    G_unified = create_unified_network(G, sources, sinks)

    # Calculate maximum flow from super source to super sink
    max_flow, flow_dict = nx.maximum_flow(
        G_unified,
        "SUPER_SOURCE",
        "SUPER_SINK",
        flow_func=nx.algorithms.flow.edmonds_karp,
    )

    # Analyze optimality for the entire network
    analysis = check_optimal_flow(G_unified, "SUPER_SOURCE", "SUPER_SINK", max_flow)

    # Extract actual terminal-to-store flows from the flow dictionary
    # We need to properly attribute flow from each terminal to each store
    # accounting for shared warehouses
    terminal_store_flows = []

    for terminal in sources:
        terminal_total_flow = flow_dict.get("SUPER_SOURCE", {}).get(terminal, 0)
        if terminal_total_flow > 0:
            # For each warehouse connected to this terminal
            for warehouse in G.successors(terminal):
                terminal_to_warehouse = flow_dict.get(terminal, {}).get(warehouse, 0)

                if terminal_to_warehouse > 0:
                    # Calculate total outgoing flow from this warehouse
                    warehouse_total_out = sum(
                        flow_dict.get(warehouse, {}).get(s, 0)
                        for s in G.successors(warehouse)
                    )

                    if warehouse_total_out > 0:
                        # For each store connected to this warehouse
                        for store in G.successors(warehouse):
                            warehouse_to_store = flow_dict.get(warehouse, {}).get(
                                store, 0
                            )

                            if warehouse_to_store > 0:
                                # Proportionally attribute the store flow to this terminal
                                # based on how much this terminal contributes to the warehouse
                                total_warehouse_in = sum(
                                    flow_dict.get(t, {}).get(warehouse, 0)
                                    for t in sources
                                )

                                if total_warehouse_in > 0:
                                    proportion = (
                                        terminal_to_warehouse / total_warehouse_in
                                    )
                                    attributed_flow = warehouse_to_store * proportion

                                    if (
                                        attributed_flow > 0.01
                                    ):  # Only include significant flows
                                        terminal_store_flows.append(
                                            (terminal, store, attributed_flow)
                                        )

    return {
        "max_flow": max_flow,
        "flow_distribution": terminal_store_flows,
        "optimality_analysis": analysis,
        "graph": G_unified,
        "flow_dict": flow_dict,
    }


def get_edges_list(G):
    """
    Returns a list of all edges in the graph with their capacities.

    Args:
        G: NetworkX DiGraph

    Returns:
        list: List of tuples (source, target, capacity)
    """
    edges = []
    for u, v, data in G.edges(data=True):
        edges.append((u, v, data.get("capacity", 0)))
    return edges


def validate_edge(G, edge_name):
    """
    Validates if an edge exists in the graph.

    Args:
        G: NetworkX DiGraph
        edge_name: String in format "source->target"

    Returns:
        tuple: (is_valid, source, target) or (False, None, None)
    """
    if "->" not in edge_name:
        return False, None, None

    parts = edge_name.split("->")
    if len(parts) != 2:
        return False, None, None

    source, target = parts[0].strip(), parts[1].strip()

    if G.has_edge(source, target):
        return True, source, target

    return False, None, None


def update_edge_capacity(G, source, target, new_capacity):
    """
    Updates the capacity of an edge in the graph.

    Args:
        G: NetworkX DiGraph
        source: Source node
        target: Target node
        new_capacity: New capacity value

    Returns:
        dict: {"success": bool, "message": str, "old_capacity": int, "new_capacity": int}
    """
    if not G.has_edge(source, target):
        return {
            "success": False,
            "message": f"Edge {source} -> {target} does not exist",
        }

    if new_capacity <= 0:
        return {
            "success": False,
            "message": f"Capacity must be positive, got {new_capacity}",
        }

    old_capacity = G[source][target]["capacity"]
    G[source][target]["capacity"] = new_capacity

    return {
        "success": True,
        "message": f"Updated edge {source} -> {target}: {old_capacity} → {new_capacity}",
        "old_capacity": old_capacity,
        "new_capacity": new_capacity,
    }


def get_edge_autocomplete_list(G):
    """
    Returns a list of edge names for autocomplete in format "source->target".

    Args:
        G: NetworkX DiGraph

    Returns:
        list: List of edge names
    """
    edges = []
    for u, v in G.edges():
        edges.append(f"{u} -> {v}")
    return edges


def get_current_state(G):
    """
    Returns current state of the network.

    Args:
        G: NetworkX DiGraph

    Returns:
        dict: Current network state with edges and their capacities
    """
    edges = get_edges_list(G)
    return {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "edges": edges,
    }
