import networkx as nx

from task_1.logistics_network_simulator.data import pos, edges
from task_1.logistics_network_simulator.build_graph import build_graph
from task_1.logistics_network_simulator.utils import (
    analyze_network_flow,
    calculate_network_max_flow,
    prepare_capacity_matrix,
)
from task_1.logistics_network_simulator.draw_graph import draw_graph
from task_1.logistics_network_simulator.draw_network_load_graph import (
    draw_network_load_graph,
)

if __name__ == "__main__":
    G = build_graph(edges)

    capacity_matrix = prepare_capacity_matrix(G)
    # print("Capacity Matrix:")
    # print(capacity_matrix)

    terminal_count = 2
    store_count = 14
    flow_pair = []
    for t in range(1, terminal_count + 1):
        for s in range(1, store_count + 1):
            flow_pair.append((f"Terminal {t}", f"Store {s}"))

    def get_node_index(node_name):
        return list(G.nodes).index(node_name)

    # Analyze network capacity
    sources = ["Terminal 1", "Terminal 2"]
    stores = [f"Store {i}" for i in range(1, 15)]
    network_analysis = analyze_network_flow(G, sources, stores)

    # =========================================================================
    # ENTIRE NETWORK ANALYSIS (Multi-Source Multi-Sink)
    # =========================================================================
    print("\n" + "=" * 70)
    print("ENTIRE NETWORK OPTIMAL FLOW ANALYSIS")
    print("(Analyzing all terminals and stores as a unified system)")
    print("=" * 70)

    # Calculate network-wide optimal flow
    network_result = calculate_network_max_flow(G, sources, stores)

    print(
        f"\nTotal Maximum Flow Through Entire Network: {network_result['max_flow']} units"
    )
    print(network_result["optimality_analysis"]["explanation"])

    print("\n" + "=" * 70)
    print("ACTUAL TERMINAL → STORE FLOW TABLE")
    print("=" * 70)
    print(f"{'Terminal':<15} {'Store':<15} {'Actual Flow (units)':<20}")
    print("-" * 50)

    for t in sources:
        for s in stores:
            actual_flow = 0
            # For each warehouse, check if it connects terminal t to store s
            for warehouse in G.successors(t):
                if warehouse.startswith("Warehouse"):
                    flow_to_warehouse = network_result["flow_dict"][t][warehouse]
                    flow_to_store = network_result["flow_dict"][warehouse][s] if s in network_result["flow_dict"][warehouse] else 0
                    # The actual flow from t to s via this warehouse is the min of the two
                    actual_flow += min(flow_to_warehouse, flow_to_store)
            print(f"{t:<15} {s:<15} {actual_flow:<20}")

    print("-" * 50)
    # Display actual flow distribution from terminals to stores
    print("\n" + "=" * 70)
    print("ACTUAL FLOW DISTRIBUTION (Terminal → Store)")
    print("(Proportional distribution when all terminals operate simultaneously)")
    print("=" * 70)

    # Calculate total store capacity
    total_store_capacity = 0
    store_capacities = {}
    for store in stores:
        capacity = sum(
            G[predecessor][store]["capacity"] for predecessor in G.predecessors(store)
        )
        store_capacities[store] = capacity
        total_store_capacity += capacity

    # Build mapping of which warehouses supply which stores
    store_to_warehouses = {}
    for store in stores:
        store_to_warehouses[store] = list(G.predecessors(store))

    # Build mapping of which terminals supply which warehouses
    warehouse_to_terminals = {}
    for warehouse in G.nodes():
        if warehouse.startswith("Warehouse"):
            warehouse_to_terminals[warehouse] = list(G.predecessors(warehouse))

    # Distribute flows proportionally to all stores based on their capacity
    print(f"{'Store':<15} {'Capacity':<12} {'Proportional':<15} {'Sources':<35}")
    print("-" * 89)

    total_distributed = 0

    for store in stores:
        store_capacity = store_capacities[store]
        # Allocate flow proportionally based on store capacity
        proportional_flow = (store_capacity / total_store_capacity) * network_result[
            "max_flow"
        ]
        total_distributed += proportional_flow

        # Find all possible sources for this store by tracing back through warehouses
        sources_for_store = {}

        # Get warehouses that supply this store
        warehouses = store_to_warehouses.get(store, [])

        for warehouse in warehouses:
            # Get terminals that supply this warehouse
            terminals = warehouse_to_terminals.get(warehouse, [])

            for terminal in terminals:
                if terminal not in sources_for_store:
                    sources_for_store[terminal] = 0
                # Distribute proportionally among all possible paths
                sources_for_store[terminal] += (
                    proportional_flow / len(terminals) if terminals else 0
                )

        if sources_for_store:
            sources_str = ", ".join(
                [f"{t}: {f:.2f}" for t, f in sorted(sources_for_store.items())]
            )
        else:
            sources_str = "No incoming warehouse"

        print(
            f"{store:<15} {store_capacity:<12} {proportional_flow:<15.2f} {sources_str:<35}"
        )

    print("-" * 82)
    print(f"{'TOTAL':<15} {total_store_capacity:<12} {total_distributed:<15.2f}")

    # =========================================================================
    # COMPARISON: Individual Path Analysis
    # =========================================================================
    print("\n\n" + "=" * 70)
    print("COMPARISON: INDIVIDUAL SOURCE-SINK PATH ANALYSIS")
    print("(Maximum possible flow if each path operated independently)")
    print("=" * 70)
    print("\nNote: These values show the THEORETICAL maximum for each path")
    print("if it were the ONLY flow in the network (not realistic).\n")

    print(f"{'Terminal':<15} {'Store':<15} {'Max Flow (units)':<15}")
    print("-" * 45)

    # Show only non-zero flows for clarity
    for pair in flow_pair:
        flow_value, _ = nx.maximum_flow(
            G,
            pair[0],
            pair[1],
            flow_func=nx.algorithms.flow.edmonds_karp,
        )
        if flow_value > 0:
            print(f"{pair[0]:<15} {pair[1]:<15} {flow_value:<15}")

    # Final Summary
    print("\n" + "=" * 70)
    print("SUMMARY AND CONCLUSIONS")
    print("=" * 70)
    print(f"\n1. ENTIRE NETWORK OPTIMAL FLOW: {network_result['max_flow']} units")
    print(f"   - This is the actual maximum throughput when all terminals")
    print(f"     and stores operate simultaneously.")
    print(
        f"   - Optimal flow achieved: {network_result['optimality_analysis']['is_optimal']}"
    )
    print(f"   - Max flow = Min cut: {network_result['max_flow']} units")

    print(f"\n2. NETWORK BOTTLENECK:")
    print(
        f"   - Total terminal capacity: {network_analysis['source_total_capacity']} units"
    )
    print(f"   - Total store capacity: {network_analysis['sink_total_capacity']} units")
    print(f"   - Actual throughput: {network_result['max_flow']} units")
    print(
        f"   - Utilization: {(network_result['max_flow'] / network_analysis['source_total_capacity'] * 100):.1f}%"
    )

    print(f"\n3. KEY INSIGHTS:")
    print(f"   - The Edmonds-Karp algorithm finds optimal flow using BFS")
    print(f"   - Optimality verified by Max-Flow Min-Cut Theorem")
    print(f"   - Flow is limited by warehouse intermediate capacities")
    print(f"   - Individual path analysis shows theoretical maximums only")
    print(f"   - Real network behavior requires unified multi-source analysis")

    print("\n" + "=" * 70 + "\n")

    print("\nGenerating network load distribution graph...")
    draw_network_load_graph(G, network_result["flow_dict"], pos, sources, stores)

    print("Generating original network graph...")
    draw_graph(G, pos)
