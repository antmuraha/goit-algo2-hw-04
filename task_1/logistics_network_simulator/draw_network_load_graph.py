import networkx as nx
import matplotlib.pyplot as plt


def draw_network_load_graph(G, flow_dict, pos, sources, stores):
    """
    Draws the network graph with node load percentages.
    Stores receive proportional flow based on their capacity relative to siblings.

    Args:
        G: NetworkX DiGraph (original network without super nodes)
        flow_dict: Flow dictionary from maximum flow calculation
        pos: Node positions dictionary
        sources: List of source terminals
        stores: List of store nodes
    """
    fig, ax = plt.subplots(figsize=(14, 10))

    # Pre-calculate proportional flows for stores
    # For each warehouse, distribute its outgoing flow proportionally to child stores
    store_proportional_flows = {}

    warehouses = [node for node in G.nodes() if node.startswith("Warehouse")]

    for warehouse in warehouses:
        # Get outgoing flow from this warehouse
        warehouse_outflow = sum(
            flow_dict.get(warehouse, {}).get(succ, 0)
            for succ in G.successors(warehouse)
        )

        # Get child stores and their capacities
        child_stores = list(G.successors(warehouse))

        if child_stores and warehouse_outflow > 0:
            # Calculate total capacity of child stores
            total_child_capacity = sum(
                sum(G[pred][store]["capacity"] for pred in G.predecessors(store))
                for store in child_stores
            )

            # Distribute warehouse flow proportionally to each store
            for store in child_stores:
                store_capacity = sum(
                    G[pred][store]["capacity"] for pred in G.predecessors(store)
                )

                if total_child_capacity > 0:
                    # Proportional share of this warehouse's flow
                    proportion = store_capacity / total_child_capacity
                    proportional_flow = warehouse_outflow * proportion

                    if store not in store_proportional_flows:
                        store_proportional_flows[store] = 0
                    store_proportional_flows[store] += proportional_flow

    # Calculate node loads
    node_colors = []
    node_sizes = []
    node_labels_with_load = {}

    # Get all nodes except super source/sink
    regular_nodes = [
        node for node in G.nodes() if node not in ["SUPER_SOURCE", "SUPER_SINK"]
    ]

    for node in regular_nodes:
        # Calculate incoming flow
        incoming_flow = sum(
            flow_dict.get(pred, {}).get(node, 0) for pred in G.predecessors(node)
        )

        # Calculate outgoing flow
        outgoing_flow = sum(
            flow_dict.get(node, {}).get(succ, 0) for succ in G.successors(node)
        )

        # For stores: use proportional flow distributed from parent warehouse
        # For others: use actual flow
        if node in stores:
            actual_flow = store_proportional_flows.get(node, 0)
        else:
            actual_flow = max(incoming_flow, outgoing_flow)

        # Calculate capacity based on node type
        if node in sources:
            # For terminals: capacity is sum of outgoing edges
            capacity = sum(G[node][succ]["capacity"] for succ in G.successors(node))
        elif node in stores:
            # For stores: capacity is the edge capacity from parent warehouse
            parent_warehouses = list(G.predecessors(node))
            if parent_warehouses:
                parent_warehouse = parent_warehouses[0]
                capacity = G[parent_warehouse][node]["capacity"]
            else:
                capacity = 1
        else:
            # For warehouses: capacity is sum of outgoing edges
            capacity = sum(G[node][succ]["capacity"] for succ in G.successors(node))

        # Calculate load percentage
        if node in stores:
            # For stores: percentage = edge_capacity_to_store / sum_of_all_edge_capacities_from_warehouse
            parent_warehouses = list(G.predecessors(node))
            if parent_warehouses:
                parent_warehouse = parent_warehouses[0]
                edge_capacity_to_store = G[parent_warehouse][node]["capacity"]
                # Get total edge capacity from parent warehouse
                total_warehouse_capacity = sum(
                    G[parent_warehouse][succ]["capacity"]
                    for succ in G.successors(parent_warehouse)
                )
                load_percent = (
                    (edge_capacity_to_store / total_warehouse_capacity * 100)
                    if total_warehouse_capacity > 0
                    else 0
                )
            else:
                load_percent = 0
        else:
            # For terminals and warehouses: percentage = actual_flow / capacity
            load_percent = (actual_flow / capacity * 100) if capacity > 0 else 0

        # Create label with node name and load percentage
        node_labels_with_load[node] = f"{node}\n({load_percent:.1f}%)"

        # Color nodes based on load: green (low) to red (high)
        if load_percent < 30:
            node_colors.append("#90EE90")  # Light green
        elif load_percent < 60:
            node_colors.append("#FFD700")  # Gold
        elif load_percent < 85:
            node_colors.append("#FFA500")  # Orange
        else:
            node_colors.append("#FF6B6B")  # Red

        # Size nodes based on load
        node_sizes.append(2000 + load_percent * 30)

    # Draw edges with arrows and offset from node center
    from matplotlib.patches import FancyArrowPatch
    import matplotlib.patches as mpatches

    for u, v in G.edges():
        if u in ["SUPER_SOURCE", "SUPER_SINK"] or v in ["SUPER_SOURCE", "SUPER_SINK"]:
            continue

        x1, y1 = pos[u]
        x2, y2 = pos[v]

        # Create arrow with offset from nodes
        arrow = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            color="gray",
            linewidth=2.5,
            mutation_scale=30,
            shrinkA=30,  # Offset from source node center
            shrinkB=30,  # Offset from destination node center
            connectionstyle="arc3,rad=0.05",
            zorder=0,
        )
        ax.add_patch(arrow)

    # Draw nodes with calculated colors and sizes
    node_collection = nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        nodelist=regular_nodes,
        node_color=node_colors,
        node_size=node_sizes,
        edgecolors="black",
        linewidths=2,
    )

    # Draw node labels with load percentages
    nx.draw_networkx_labels(
        G, pos, labels=node_labels_with_load, ax=ax, font_size=9, font_weight="bold"
    )

    # Calculate load percentages for all nodes first (reuse logic)
    node_load_percent = {}

    for node in regular_nodes:
        # Calculate incoming flow
        incoming_flow = sum(
            flow_dict.get(pred, {}).get(node, 0) for pred in G.predecessors(node)
        )

        # Calculate outgoing flow
        outgoing_flow = sum(
            flow_dict.get(node, {}).get(succ, 0) for succ in G.successors(node)
        )

        # For stores: use proportional flow distributed from parent warehouse
        # For others: use actual flow
        if node in stores:
            actual_flow = store_proportional_flows.get(node, 0)
        else:
            actual_flow = max(incoming_flow, outgoing_flow)

        # Calculate capacity based on node type
        if node in sources:
            # For terminals: capacity is sum of outgoing edges
            capacity = sum(G[node][succ]["capacity"] for succ in G.successors(node))
        elif node in stores:
            # For stores: capacity is the edge capacity from parent warehouse
            parent_warehouses = list(G.predecessors(node))
            if parent_warehouses:
                parent_warehouse = parent_warehouses[0]
                capacity = G[parent_warehouse][node]["capacity"]
            else:
                capacity = 1
        else:
            # For warehouses: capacity is sum of outgoing edges
            capacity = sum(G[node][succ]["capacity"] for succ in G.successors(node))

        # Calculate load percentage
        if node in stores:
            # For stores: percentage = edge_capacity_to_store / sum_of_all_edge_capacities_from_warehouse
            parent_warehouses = list(G.predecessors(node))
            if parent_warehouses:
                parent_warehouse = parent_warehouses[0]
                edge_capacity_to_store = G[parent_warehouse][node]["capacity"]
                # Get total edge capacity from parent warehouse
                total_warehouse_capacity = sum(
                    G[parent_warehouse][succ]["capacity"]
                    for succ in G.successors(parent_warehouse)
                )
                load_percent = (
                    (edge_capacity_to_store / total_warehouse_capacity * 100)
                    if total_warehouse_capacity > 0
                    else 0
                )
            else:
                load_percent = 0
        else:
            # For terminals and warehouses: percentage = actual_flow / capacity
            load_percent = (actual_flow / capacity * 100) if capacity > 0 else 0

        node_load_percent[node] = load_percent

    # Draw edge labels (capacities with actual flow from flow_dict)
    edge_labels = {}
    for u, v in G.edges():
        if u in ["SUPER_SOURCE", "SUPER_SINK"] or v in ["SUPER_SOURCE", "SUPER_SINK"]:
            continue

        capacity = G[u][v]["capacity"]

        # For edges to stores: show proportional allocation of warehouse flow
        if v in stores:
            # Get the warehouse (u) actual outflow
            warehouse_actual_flow = sum(
                flow_dict.get(u, {}).get(succ, 0) for succ in G.successors(u)
            )

            # Get total warehouse capacity
            total_warehouse_capacity = sum(
                G[u][succ]["capacity"] for succ in G.successors(u)
            )

            # Calculate proportional flow to this store
            if total_warehouse_capacity > 0:
                proportion = capacity / total_warehouse_capacity
                flow_on_edge = warehouse_actual_flow * proportion
            else:
                flow_on_edge = 0
        else:
            # For other edges: use actual flow from flow_dict
            flow_on_edge = flow_dict.get(u, {}).get(v, 0)

        # Format: "capacity [flow]"
        edge_labels[(u, v)] = f"{int(capacity)} [{int(round(flow_on_edge))}]"

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=8)

    # Add title and legend
    ax.set_title(
        "Network Load Distribution - Warehouse and Store Utilization\n(Warehouses: load% = flow/capacity | Stores: load% = edge_capacity/sum_of_warehouse_edges)",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )

    # Add legend
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor="#90EE90", edgecolor="black", label="Load < 30% (Low)"),
        Patch(facecolor="#FFD700", edgecolor="black", label="Load 30-60% (Medium)"),
        Patch(facecolor="#FFA500", edgecolor="black", label="Load 60-85% (High)"),
        Patch(facecolor="#FF6B6B", edgecolor="black", label="Load > 85% (Critical)"),
    ]
    ax.legend(
        handles=legend_elements,
        loc="upper center",
        fontsize=10,
    )

    ax.axis("off")
    plt.tight_layout()
    plt.show()
