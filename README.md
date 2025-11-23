# QoS Queuing Strategies Simulation

A comprehensive implementation and experimental analysis of Quality of Service (QoS) queuing strategies for network packet processing with **realistic bursty traffic patterns**.

## Overview

This project implements and compares four fundamental queuing strategies:

1. **First-Come, First-Served (FCFS)** - Processes packets in arrival order
2. **Priority Queuing (PQ)** - Processes higher priority packets first
3. **Round-Robin (RR)** - Distributes packets across multiple queues and serves them cyclically
4. **Fair Queueing (FQ)** - Maintains per-flow queues with virtual finish times for fairness

## Features

- **Complete Implementation**: Full Python implementation of four queuing strategies from scratch
- **Realistic Traffic Model**: Bursty traffic generation that better represents real-world network behavior (video streaming, file downloads, web browsing)
- **Finite Queue Capacity**: Support for limited buffer sizes with packet dropping (configurable)
- **Dual Fairness Metrics**: Measures both per-packet and per-flow fairness to show trade-offs
- **Performance Metrics**: Measures latency, throughput, fairness, and drop rates for each strategy
- **Comprehensive Testing**: Multiple experimental scenarios including high traffic, priority stress tests, and variable service times
- **Visualization**: Detailed graphs and charts comparing strategy performance using matplotlib

## Project Structure

```
.
├── packet.py                  # Packet class definition
├── queuing_strategies.py      # Implementation of all four queuing strategies
├── simulation.py              # Packet generation and simulation framework
├── visualization.py           # Visualization and plotting utilities
├── main.py                    # Main simulation runner with 5 experiments
├── example.py                 # Simple example demonstrating basic usage
├── demo_packet_dropping.py    # Demonstration of packet dropping with finite queues
├── custom_simulation.py       # Interactive/CLI tool for custom simulations
├── test_queuing.py            # Unit tests for all components
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore patterns
└── results/                   # Output directory for generated plots
    ├── .gitkeep
    ├── basic_comparison.png
    ├── high_traffic_latency.png
    ├── priority_fairness.png
    ├── variable_service_fairness.png
    └── latency_distribution.png
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Zach1113/NYCU-WMN.git
cd NYCU-WMN
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the simple example to see the basic functionality:

```bash
python example.py
```

### Running Custom Simulations

Use the custom simulation script to run experiments with your own parameters:

```bash
# Interactive mode
python custom_simulation.py

# Command-line mode
python custom_simulation.py <num_packets> <arrival_rate> <high_priority_ratio> <seed>

# Example: 200 packets, 3.0 arrival rate, 30% high priority, seed 42
python custom_simulation.py 200 3.0 0.3 42
```

### Running the Full Simulation

Execute the main simulation script to run all experiments:

```bash
python main.py
```

This will:
- Run 5 different experimental scenarios
- Generate performance metrics for each strategy
- Create visualization plots in the `results/` directory
- Print comprehensive performance comparisons to console

### Running Tests

Execute the unit tests to verify functionality:

```bash
python test_queuing.py
```

### Packet Dropping Demonstration

See how strategies handle congestion with finite queue capacity:

```bash
python demo_packet_dropping.py
```

This demonstrates:
- Packet dropping when queues are full
- Drop rates under different congestion levels
- Per-flow drop distribution
- Comparison between infinite and finite queue capacities

### Custom Experiments

You can create custom experiments by using the provided modules:

```python
from packet import Packet
from queuing_strategies import FCFSQueue, PriorityQueue, RoundRobinQueue, FairQueue
from simulation import PacketGenerator, Simulator, run_experiment
from visualization import plot_all_metrics

# Generate packets with bursty traffic (default)
generator = PacketGenerator(seed=42)
packets = generator.generate_packets(
    num_packets=100,
    arrival_rate=2.0,
    priority_distribution={1: 0.5, 2: 0.3, 3: 0.2}
)

# Create strategies (with optional finite queue capacity)
strategies = [
    FCFSQueue(),                    # Infinite capacity
    FCFSQueue(max_queue_size=50),   # Finite capacity (drops when full)
    PriorityQueue(),
    RoundRobinQueue(num_queues=3),
    FairQueue(max_queue_size=50)    # Fair Queue with finite capacity
]

# Run experiment and visualize
results = run_experiment(packets, strategies)
plot_all_metrics(results, save_path='my_results.png')

# Check drop rates
for name, metrics in results.items():
    print(f"{name}: {metrics['dropped_packets']} dropped ({metrics['drop_rate']*100:.1f}%)")
```

## Experimental Scenarios

The simulation includes five comprehensive experiments:

1. **Basic Comparison**: Moderate traffic with mixed priorities
2. **High Traffic Load**: Stress test with 500 packets and high arrival rate
3. **Priority Stress Test**: Heavy load of high-priority packets
4. **Variable Service Times**: Wide range of packet processing times
5. **Latency Distribution Analysis**: Detailed statistical analysis

## Performance Metrics

Each strategy is evaluated on:

- **Average Latency**: Total delay from arrival to completion
- **Average Waiting Time**: Time spent waiting in queue
- **Throughput**: Packets processed per unit time
- **Dropped Packets**: Number of packets dropped when queue is full (if finite capacity)
- **Drop Rate**: Percentage of offered packets that were dropped
- **Flow Fairness**: Jain's fairness index on average latency per flow (measures how equally flows are served)

## Understanding Flow Fairness

This project focuses on **Per-Flow Fairness** (Jain's Fairness Index) as the primary metric for QoS:

- **What it measures**: How equally different flows (groups of packets) are served
- **Why it matters**: In multi-tenant systems, we want to prevent aggressive flows from starving small flows
- **The Goal**: A value close to 1.0 means all flows receive equal service quality
- **Fair Queue's Advantage**: By using virtual finish times and per-flow queues, Fair Queue achieves superior flow fairness compared to FCFS.

## Traffic Model

The simulation uses a **bursty traffic model** to represent real-world network behavior:

- **Bursty arrivals**: Flows send packets in bursts (like video streaming, file downloads)
- **Realistic patterns**: Better demonstrates Fair Queue's benefits compared to random (Poisson) arrivals
- **Configurable**: Can switch to Poisson model with `traffic_model='poisson'` parameter

## Key Findings

From the experimental results with bursty traffic:

- **FCFS**: Good per-packet fairness but doesn't actively protect small flows
- **Priority Queue**: Efficiently handles high-priority packets but intentionally unfair (may starve low-priority traffic)
- **Round-Robin**: Balances load across queues with good per-packet fairness
- **Fair Queue**: **Best per-flow fairness** (0.90+) - actively protects small flows from large bursts, ideal for multi-tenant systems

## Implementation Details

### Packet Class
- Stores packet metadata (id, arrival_time, priority, size, service_time)
- Tracks timing information (start_time, finish_time)
- Calculates latency and waiting time

### Queuing Strategies
- **FCFS**: Uses `collections.deque` for FIFO processing
- **Priority Queue**: Uses `heapq` for priority-based processing
- **Round-Robin**: Maintains multiple queues with cyclic scheduling
- **Fair Queue**: Maintains per-flow queues with virtual finish time calculation for max-min fairness

### Queue Capacity & Dropping Policies

All strategies support configurable `max_queue_size`. When the limit is reached:

- **FCFS / Priority / Round-Robin**: Use **Global Tail Drop**. The queue is shared globally; if one flow fills it (e.g., arrives first), subsequent packets from any flow are dropped.
- **Fair Queue**: Uses **Per-Flow Fair Dropping**. The buffer space is dynamically partitioned among active flows. This prevents aggressive flows from hogging the buffer and ensures small flows still get space during congestion.

### Simulation Framework
- Generates packets with bursty arrival patterns (default) or Poisson process
- Supports configurable priority and size distributions
- Event-driven simulation with accurate timing
- Realistic traffic model representing video, downloads, and web traffic

## Requirements

- Python 3.7+
- matplotlib >= 3.5.0
- numpy >= 1.21.0

## License

This project is developed for educational purposes as part of NYCU Wireless and Mobile Networks coursework.

## Author

Zach1113

## Acknowledgments

This implementation is based on standard queueing theory and network QoS principles.
