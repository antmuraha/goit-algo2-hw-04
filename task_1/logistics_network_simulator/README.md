# Logistics Network Simulator - Quick Start Guide

## Run Simulator

```bash
cd task_1/logistics_network_simulator
python .
```

---

## Interactive Session Examples

### Example 1: View Network Status

```
Logistics Network Simulator - Interactive Console Application

╭────────────────────────────────────────────────────────────────╮
│                 Logistics Network Simulator                    │
│          Interactive console app for managing logistics        │
│                          networks                              │
│                                                                │
│ Available Commands:                                            │
│   draw     - Visualize the network                             │
│   set      - Update edge capacity                              │
|   maxflow  - Find max flow from source to sink (by index)      |
|   maxflow-analisis - Analyze max flow with optimality details  |
│   status   - Show network status                               │
│   help     - Show help                                         │
│   exit     - Exit application                                  │
│                                                                │
│ Use draw --help or set --help for more details.                │
╰────────────────────────────────────────────────────────────────╯
✓ Network loaded with 20 nodes and 20 edges

network>> status
  Network Status
┏━━━━━━━━┳━━━━━━━┓
┃ Metric ┃ Value ┃
┡━━━━━━━━╇━━━━━━━┩
│ Nodes  │ 20    │
│ Edges  │ 20    │
└────────┴───────┘
  Sources Index
┏━━━┳━━━━━━━━━━━━┓
┃ # ┃ Source     ┃
┡━━━╇━━━━━━━━━━━━┩
│ 1 │ Terminal 1 │
│ 2 │ Terminal 2 │
└───┴────────────┘
  Targets Index
┏━━━━┳━━━━━━━━━━┓
┃ #  ┃ Target   ┃
┡━━━━╇━━━━━━━━━━┩
│ 1  │ Store 1  │
│ 2  │ Store 2  │
│ 3  │ Store 3  │
│ 4  │ Store 4  │
│ 5  │ Store 5  │
│ 6  │ Store 6  │
│ 7  │ Store 7  │
│ 8  │ Store 8  │
│ 9  │ Store 9  │
│ 10 │ Store 10 │
│ 11 │ Store 11 │
│ 12 │ Store 12 │
│ 13 │ Store 13 │
│ 14 │ Store 14 │
└────┴──────────┘
                Network Edges
┏━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ #  ┃ Source      ┃ Target      ┃ Capacity ┃
┡━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 1  │ Terminal 1  │ Warehouse 1 │ 25       │
│ 2  │ Terminal 1  │ Warehouse 2 │ 20       │
│ 3  │ Terminal 1  │ Warehouse 3 │ 15       │
│ 4  │ Warehouse 1 │ Store 1     │ 15       │
│ 5  │ Warehouse 1 │ Store 2     │ 10       │
│ 6  │ Warehouse 1 │ Store 3     │ 20       │
│ 7  │ Warehouse 2 │ Store 4     │ 15       │
│ 8  │ Warehouse 2 │ Store 5     │ 10       │
│ 9  │ Warehouse 2 │ Store 6     │ 25       │
│ 10 │ Warehouse 3 │ Store 7     │ 20       │
│ 11 │ Warehouse 3 │ Store 8     │ 15       │
│ 12 │ Warehouse 3 │ Store 9     │ 10       │
│ 13 │ Terminal 2  │ Warehouse 3 │ 15       │
│ 14 │ Terminal 2  │ Warehouse 4 │ 30       │
│ 15 │ Terminal 2  │ Warehouse 2 │ 10       │
│ 16 │ Warehouse 4 │ Store 10    │ 20       │
│ 17 │ Warehouse 4 │ Store 11    │ 10       │
│ 18 │ Warehouse 4 │ Store 12    │ 15       │
│ 19 │ Warehouse 4 │ Store 13    │ 5        │
│ 20 │ Warehouse 4 │ Store 14    │ 10       │
└────┴─────────────┴─────────────┴──────────┘
```

---

### Example 4: Draw Visualization

```
network>> draw
Rendering basic visualization...
✓ Visualization complete
```

```
network>> draw load
Rendering load visualization...
✓ Visualization complete
```

---

### Example 5: Reset Network

```
network>> reset
✓ Network reset to original state
...

```

---

### Example 6: Help & Exit

```
network>> help
Logistics Network Simulator - Help

Commands:

    draw basic(default)|load
        Visualize the logistics network
        Options:
            basic  - Basic network diagram with edges and capacities
            load   - Network visualization with load analysis

    set INDEX VALUE
        Update the capacity of a network edge
        INDEX  - Row number from the Network Edges table (starting at 1)
        VALUE  - New capacity value (positive integer)
        Example: set 2 50

    maxflow SOURCE_INDEX SINK_INDEX [FUNCTION]
        Find the maximum flow from a source to a sink by their indices.
        FUNCTION: 'networkx' (default, uses Edmonds-Karp) or 'custom' (uses custom logic)
        Example: maxflow 1 3
        Example: maxflow 1 3 custom

    maxflow-analisis SOURCE_INDEX SINK_INDEX
        Analyze the max flow between source and sink, showing optimality and bottleneck details.
        Example: maxflow-analisis 1 3

    status
        Display current network status and all edge capacities

    reset
        Reset all edge capacities to their original values

    help

    exit
        Exit the application

Examples:
    draw basic
    draw load
    maxflow 1 3
    maxflow-analisis 1 3
    maxflow 1 3
    maxflow 1 3 custom
    status
    reset

network>> exit
Exiting Logistics Network Simulator...
```
