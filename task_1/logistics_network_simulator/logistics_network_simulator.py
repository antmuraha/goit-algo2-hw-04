"""
Logistics Network Simulator - Interactive Console Application
Manages and analyzes logistics networks with real-time edge capacity updates.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

from data import edges, pos
from build_graph import build_graph
from draw_graph import draw_graph
from draw_network_load_graph import draw_network_load_graph
from utils import (
    validate_edge,
    update_edge_capacity,
    get_edge_autocomplete_list,
    get_current_state,
    calculate_network_max_flow,
)

app = typer.Typer(
    help="Logistics Network Simulator - Manage and analyze logistics networks"
)
console = Console()

# Global state - network initialized at startup
network_state = {
    "graph": None,
    "original_edges": None,
    "pos": pos,
    "sources": ["Terminal 1", "Terminal 2"],
    "sinks": [f"Store {i}" for i in range(1, 15)],
}


def initialize_network():
    """Initialize the logistics network from data."""
    network_state["graph"] = build_graph(edges)
    network_state["original_edges"] = [(e[0], e[1], e[2]) for e in edges]


def print_welcome():
    """Print welcome message with instructions."""
    welcome_text = """
[bold cyan]Logistics Network Simulator[/bold cyan]
Interactive console app for managing logistics networks

[yellow]Available Commands:[/yellow]
    [bold]draw[/bold]     - Visualize the network
    [bold]set[/bold]      - Update edge capacity
    [bold]maxflow[/bold]  - Find max flow from source to sink (by index)
    [bold]maxflow-analisis[/bold] - Analyze max flow with optimality details
    [bold]status[/bold]   - Show network status
    [bold]help[/bold]     - Show help
    [bold]exit[/bold]     - Exit application

Use [cyan]draw --help[/cyan] or [cyan]set --help[/cyan] for more details.
        """
    console.print(Panel(welcome_text, border_style="cyan"))


def print_network_info():
    """Print current network information."""
    state = get_current_state(network_state["graph"])

    table = Table(title="Network Status", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="dim")
    table.add_column("Value", style="green")

    table.add_row("Nodes", str(state["num_nodes"]))
    table.add_row("Edges", str(state["num_edges"]))

    console.print(table)

    # Print index table for Sources
    sources = network_state.get("sources", [])
    if sources:
        sources_table = Table(
            title="Sources Index", show_header=True, header_style="bold magenta"
        )
        sources_table.add_column("#", style="bold yellow")
        sources_table.add_column("Source", style="cyan")
        for idx, source in enumerate(sources, start=1):
            sources_table.add_row(str(idx), source)
        console.print(sources_table)

    # Print index table for Targets
    sinks = network_state.get("sinks", [])
    if sinks:
        sinks_table = Table(
            title="Targets Index", show_header=True, header_style="bold magenta"
        )
        sinks_table.add_column("#", style="bold yellow")
        sinks_table.add_column("Target", style="cyan")
        for idx, sink in enumerate(sinks, start=1):
            sinks_table.add_row(str(idx), sink)
        console.print(sinks_table)

    # Print edges table
    edges_table = Table(
        title="Network Edges", show_header=True, header_style="bold cyan"
    )
    edges_table.add_column("#", style="bold yellow")
    edges_table.add_column("Source", style="cyan")
    edges_table.add_column("Target", style="cyan")
    edges_table.add_column("Capacity", style="green")

    for idx, (source, target, capacity) in enumerate(state["edges"], start=1):
        edges_table.add_row(str(idx), source, target, str(capacity))

    console.print(edges_table)


def edge_autocomplete(incomplete: str) -> list[str]:
    """Autocomplete function for edge names."""
    if network_state["graph"] is None:
        return []

    available_edges = get_edge_autocomplete_list(network_state["graph"])
    return [e for e in available_edges if e.lower().startswith(incomplete.lower())]


def set_capacity(edge: str, value: int):
    """Update the capacity of a network edge by edge name (internal use)."""
    if network_state["graph"] is None:
        console.print("[red]Error: Network not initialized[/red]")
        return
    is_valid, source, target = validate_edge(network_state["graph"], edge)
    if not is_valid:
        console.print(f"[red]Invalid edge format: '{edge}'[/red]")
        return
    result = update_edge_capacity(network_state["graph"], source, target, value)
    if result["success"]:
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Property", style="dim")
        table.add_column("Value", style="green")
        table.add_row("Edge", f"{source} \u2192 {target}")
        table.add_row("Old Capacity", str(result["old_capacity"]))
        table.add_row("New Capacity", str(result["new_capacity"]))
        console.print(f"[green]\u2713 {result['message']}[/green]")
        console.print(table)
    else:
        console.print(f"[red]\u2717 {result['message']}[/red]")


@app.command()
def draw(option: str = typer.Option("basic", help="basic or load visualization")):
    """
    Draw the logistics network graph.

    Options:
      - basic: Basic network diagram
      - load: Network with load analysis
    """
    if not isinstance(option, str):
        option = "basic"

    if network_state["graph"] is None:
        console.print("[red]Error: Network not initialized[/red]")
        return

    if option.lower() not in ["basic", "load"]:
        console.print(f"[red]Invalid option '{option}'. Use 'basic' or 'load'[/red]")
        return

    try:
        console.print(f"[yellow]Rendering {option} visualization...[/yellow]")

        if option.lower() == "basic":
            draw_graph(network_state["graph"], network_state["pos"])
        else:  # load
            # Calculate flow for load visualization
            flow_result = calculate_network_max_flow(
                network_state["graph"], network_state["sources"], network_state["sinks"]
            )
            draw_network_load_graph(
                network_state["graph"],
                flow_result["flow_dict"],
                network_state["pos"],
                network_state["sources"],
                network_state["sinks"],
            )

        console.print("[green]✓ Visualization complete[/green]")
    except Exception as e:
        console.print(f"[red]Error rendering visualization: {e}[/red]")


# @app.command()
# def set_capacity(
#     edge: str = typer.Argument(..., help="Edge in format 'Source -> Target'"),
#     value: int = typer.Argument(..., help="New capacity value"),
# ):
#     """
#     Update the capacity of a network edge.

#     Example:
#       set "Terminal 1 -> Warehouse 1" 50
#     """
#     if network_state["graph"] is None:
#         console.print("[red]Error: Network not initialized[/red]")
#         return

#     # Validate edge format
#     is_valid, source, target = validate_edge(network_state["graph"], edge)

#     if not is_valid:
#         # Try to help user find correct edge format
#         available = get_edge_autocomplete_list(network_state["graph"])
#         console.print(f"[red]Invalid edge format: '{edge}'[/red]")
#         console.print("[cyan]Available edges sample:[/cyan]")
#         for i, e in enumerate(available[:5]):
#             console.print(f"  {e}")
#         if len(available) > 5:
#             console.print(f"  ... and {len(available) - 5} more")
#         return

#     # Update capacity
#     result = update_edge_capacity(network_state["graph"], source, target, value)

#     if result["success"]:
#         console.print(f"[green]✓ {result['message']}[/green]")

#         # Show updated edge info
#         table = Table(show_header=True, header_style="bold cyan")
#         table.add_column("Property", style="dim")
#         table.add_column("Value", style="green")
#         table.add_row("Edge", f"{source} → {target}")
#         table.add_row("Old Capacity", str(result["old_capacity"]))
#         table.add_row("New Capacity", str(result["new_capacity"]))
#         console.print(table)
#     else:
#         console.print(f"[red]✗ {result['message']}[/red]")


@app.command()
def status():
    """Display current network status and edge capacities."""
    if network_state["graph"] is None:
        console.print("[red]Error: Network not initialized[/red]")
        return

    print_network_info()


@app.command()
def reset():
    """Reset all edge capacities to original values."""
    if network_state["graph"] is None:
        console.print("[red]Error: Network not initialized[/red]")
        return

    # Rebuild graph with original edges
    initialize_network()
    console.print("[green]✓ Network reset to original state[/green]")
    print_network_info()


@app.command()
def help_cmd():
    """Display help information."""
    console.print("""
[bold cyan]Logistics Network Simulator - Help[/bold cyan]

[bold]Commands:[/bold]

    [cyan]draw[/cyan] basic(default)|load
        Visualize the logistics network
        Options:
            basic  - Basic network diagram with edges and capacities
            load   - Network visualization with load analysis

    [cyan]set[/cyan] INDEX VALUE
        Update the capacity of a network edge
        INDEX  - Row number from the Network Edges table (starting at 1)
        VALUE  - New capacity value (positive integer)
        Example: set 2 50

    [cyan]maxflow[/cyan] SOURCE_INDEX SINK_INDEX [FUNCTION]
        Find the maximum flow from a source to a sink by their indices.
        FUNCTION: 'networkx' (default, uses Edmonds-Karp) or 'custom' (uses custom logic)
        Example: maxflow 1 3
        Example: maxflow 1 3 custom

    [cyan]maxflow-analisis[/cyan] SOURCE_INDEX SINK_INDEX
        Analyze the max flow between source and sink, showing optimality and bottleneck details.
        Example: maxflow-analisis 1 3

    [cyan]status[/cyan]
        Display current network status and all edge capacities

    [cyan]reset[/cyan]
        Reset all edge capacities to their original values

    [cyan]help[/cyan]

    [cyan]exit[/cyan]
        Exit the application

[bold]Examples:[/bold]
    draw basic
    draw load
    maxflow 1 3
    maxflow-analisis 1 3
    maxflow 1 3
    maxflow 1 3 custom
    status
    reset
        """)


@app.command()
def main():
    """Main interactive loop for the console application."""
    # Initialize network
    initialize_network()

    # Print welcome message
    print_welcome()
    console.print(
        f"[green]✓ Network loaded with {len(network_state['graph'].nodes())} nodes and {len(network_state['graph'].edges())} edges[/green]\n"
    )

    # Interactive loop
    while True:
        try:
            user_input = Prompt.ask("[bold cyan]network>>[/bold cyan]")
            if not user_input.strip():
                continue
            command = user_input.strip().lower()
            if command == "exit":
                console.print("[yellow]Exiting Logistics Network Simulator...[/yellow]")
                break
            elif command == "status":
                print_network_info()
            elif command.startswith("draw"):
                parts = command.split()
                if len(parts) == 1:
                    draw()
                elif len(parts) == 2 and parts[1] in ["basic", "load"]:
                    draw(parts[1])
                else:
                    console.print(
                        "[red]Invalid draw command. Use 'draw basic' or 'draw load'[/red]"
                    )
            elif command.startswith("set "):
                parts = command[4:].strip().split()
                if len(parts) == 2:
                    idx_str, value_str = parts
                    try:
                        idx = int(idx_str)
                        value = int(value_str)
                        state = get_current_state(network_state["graph"])
                        edges = state["edges"]
                        if 1 <= idx <= len(edges):
                            source, target, _ = edges[idx - 1]
                            set_capacity(f"{source} -> {target}", value)
                        else:
                            console.print(
                                f"[red]Error: Index {idx} is out of range (1-{len(edges)})[/red]"
                            )
                    except ValueError:
                        console.print(
                            "[red]Error: Both INDEX and VALUE must be integers[/red]"
                        )
                else:
                    console.print(
                        "[red]Error: set command requires INDEX and VALUE[/red]"
                    )
                    console.print("Usage: set INDEX VALUE")
            elif command == "reset":
                reset()
            elif command in ["help", "?"]:
                help_cmd()
            elif command.startswith("maxflow-analisis"):
                parts = command.split()
                if len(parts) < 3:
                    console.print(
                        "[red]Usage: maxflow-analisis SOURCE_INDEX SINK_INDEX\nExample: maxflow-analisis 1 3[/red]"
                    )
                    continue
                try:
                    source_idx = int(parts[1])
                    sink_idx = int(parts[2])
                    sources = network_state.get("sources", [])
                    sinks = network_state.get("sinks", [])
                    if not (1 <= source_idx <= len(sources)):
                        console.print(
                            f"[red]Source index {source_idx} out of range (1-{len(sources)})[/red]"
                        )
                        continue
                    if not (1 <= sink_idx <= len(sinks)):
                        console.print(
                            f"[red]Sink index {sink_idx} out of range (1-{len(sinks)})[/red]"
                        )
                        continue
                    source = sources[source_idx - 1]
                    sink = sinks[sink_idx - 1]
                    G = network_state["graph"]
                    from .utils import calculate_network_max_flow

                    result = calculate_network_max_flow(G, [source], [sink])
                    max_flow = result["max_flow"]
                    console.print(
                        f"[green]Max Flow Analysis from '{source}' to '{sink}': {max_flow}[/green]"
                    )
                    console.print(result["optimality_analysis"]["explanation"])
                except Exception as e:
                    console.print(f"[red]Error running maxflow-analisis: {e}[/red]")
            elif command.startswith("maxflow"):
                parts = command.split()
                if len(parts) < 3:
                    console.print(
                        "[red]Usage: maxflow SOURCE_INDEX SINK_INDEX [FUNCTION]\nExample: maxflow 1 3 networkx[/red]"
                    )
                    continue
                try:
                    source_idx = int(parts[1])
                    sink_idx = int(parts[2])
                    func = parts[3] if len(parts) > 3 else "networkx"
                    sources = network_state.get("sources", [])
                    sinks = network_state.get("sinks", [])
                    if not (1 <= source_idx <= len(sources)):
                        console.print(
                            f"[red]Source index {source_idx} out of range (1-{len(sources)})[/red]"
                        )
                        continue
                    if not (1 <= sink_idx <= len(sinks)):
                        console.print(
                            f"[red]Sink index {sink_idx} out of range (1-{len(sinks)})[/red]"
                        )
                        continue
                    source = sources[source_idx - 1]
                    sink = sinks[sink_idx - 1]
                    G = network_state["graph"]
                    if func == "custom":
                        from .utils import calculate_network_max_flow

                        result = calculate_network_max_flow(G, [source], [sink])
                        max_flow = result["max_flow"]
                        console.print(
                            f"[green]Custom Max Flow from '{source}' to '{sink}': {max_flow}[/green]"
                        )
                    else:
                        from edmonds_karp import (
                            edmonds_karp,
                        )
                        from .utils import prepare_capacity_matrix

                        capacity_matrix = prepare_capacity_matrix(G)
                        node_list = list(G.nodes())
                        source_idx = node_list.index(source)
                        sink_idx = node_list.index(sink)
                        result = edmonds_karp(capacity_matrix, source_idx, sink_idx)
                        console.print(
                            f"[green]Edmonds-Karp Max Flow from '{source}' to '{sink}': {result['max_flow']}[/green]"
                        )
                except Exception as e:
                    console.print(f"[red]Error running maxflow: {e}[/red]")
            else:
                console.print(f"[yellow]Unknown command: '{command}'[/yellow]")
                console.print("[cyan]Type 'help' for available commands[/cyan]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
        except typer.Exit:
            raise
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


def logistics_network_simulator():
    """Entry point for the logistics network simulator."""
    pass


if __name__ == "__main__":
    app()
