# Task 1. Application of the maximum flow algorithm for goods logistics

## Run calculate maximum goods flow script

```bash
# Initial data
cat logistics_network_simulator/data.py

# Run analysis
python calculate_max_goods_flow.py

# OR run the terminale simulator
cd logistics_network_simulator
python .

```

---

Note:
To see [Logistics Network Simulator link](./logistics_network_simulator/README.md)

## Output

```
======================================================================
NETWORK CAPACITY ANALYSIS
======================================================================
Total capacity from all sources (terminals): 115 units
Total capacity to all sinks (stores): 200 units
Theoretical maximum possible flow: 115 units
======================================================================


======================================================================
ENTIRE NETWORK OPTIMAL FLOW ANALYSIS
(Analyzing all terminals and stores as a unified system)
======================================================================

Total Maximum Flow Through Entire Network: 115 units

======================================================================
OPTIMAL FLOW ANALYSIS
======================================================================
Maximum Flow: 115 units
Minimum Cut Value: 115 units
Total Capacity from SUPER_SOURCE: 115 units
Total Capacity to SUPER_SINK: 200 units
----------------------------------------------------------------------
✓ OPTIMAL FLOW ACHIEVED!
The flow is optimal because the value of the maximum flow equals the capacity of the minimum cut.
No augmenting path exists from SUPER_SOURCE to SUPER_SINK in the residual graph, therefore the flow cannot be increased.

By the Max-Flow Min-Cut Theorem:
  - The maximum flow (115) equals the minimum cut (115)
  - This means no augmenting path exists in the residual graph
  - The flow cannot be increased further

  - The source 'SUPER_SOURCE' is fully saturated
    (all 115 units of outgoing capacity are used)

  The network bottleneck is 115 units.
======================================================================


======================================================================
ACTUAL FLOW DISTRIBUTION (Terminal → Store)
(Proportional distribution when all terminals operate simultaneously)
======================================================================
Store           Capacity     Proportional    Sources
-----------------------------------------------------------------------------------------
Store 1         15           8.62            Terminal 1: 8.62
Store 10        20           11.50           Terminal 2: 11.50
Store 11        10           5.75            Terminal 2: 5.75
Store 12        15           8.62            Terminal 2: 8.62
Store 13        5            2.88            Terminal 2: 2.88
Store 14        10           5.75            Terminal 2: 5.75
Store 2         10           5.75            Terminal 1: 5.75
Store 3         20           11.50           Terminal 1: 11.50
Store 4         15           8.62            Terminal 1: 4.31, Terminal 2: 4.31
Store 5         10           5.75            Terminal 1: 2.88, Terminal 2: 2.88
Store 6         25           14.38           Terminal 1: 7.19, Terminal 2: 7.19
Store 7         20           11.50           Terminal 1: 5.75, Terminal 2: 5.75
Store 8         15           8.62            Terminal 1: 4.31, Terminal 2: 4.31
Store 9         10           5.75            Terminal 1: 2.88, Terminal 2: 2.88
----------------------------------------------------------------------------------
TOTAL           200          115.00


======================================================================
COMPARISON: INDIVIDUAL SOURCE-SINK PATH ANALYSIS
(Maximum possible flow if each path operated independently)
======================================================================

Note: These values show the THEORETICAL maximum for each path
if it were the ONLY flow in the network (not realistic).

Terminal        Store           Max Flow (units)
---------------------------------------------
Terminal 1      Store 1         15
Terminal 1      Store 2         10
Terminal 1      Store 3         20
Terminal 1      Store 4         15
Terminal 1      Store 5         10
Terminal 1      Store 6         20
Terminal 1      Store 7         15
Terminal 1      Store 8         15
Terminal 1      Store 9         10
Terminal 2      Store 4         10
Terminal 2      Store 5         10
Terminal 2      Store 6         10
Terminal 2      Store 7         15
Terminal 2      Store 8         15
Terminal 2      Store 9         10
Terminal 2      Store 10        20
Terminal 2      Store 11        10
Terminal 2      Store 12        15
Terminal 2      Store 13        5
Terminal 2      Store 14        10

======================================================================
SUMMARY AND CONCLUSIONS
======================================================================

1. ENTIRE NETWORK OPTIMAL FLOW: 115 units
   - This is the actual maximum throughput when all terminals
     and stores operate simultaneously.
   - Optimal flow achieved: True
   - Max flow = Min cut: 115 units

2. NETWORK BOTTLENECK:
   - Total terminal capacity: 115 units
   - Total store capacity: 200 units
   - Actual throughput: 115 units
   - Utilization: 100.0%

3. KEY INSIGHTS:
   - The Edmonds-Karp algorithm finds optimal flow using BFS
   - Optimality verified by Max-Flow Min-Cut Theorem
   - Flow is limited by warehouse intermediate capacities
   - Individual path analysis shows theoretical maximums only
   - Real network behavior requires unified multi-source analysis

======================================================================


Generating network load distribution graph...
Generating original network graph...
```
