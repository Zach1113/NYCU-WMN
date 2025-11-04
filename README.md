# QoS Queuing Strategies Simulation

A comprehensive implementation and experimental analysis of Quality of Service (QoS) queuing strategies for network packet processing.

## Overview

This project implements and compares three fundamental queuing strategies:

1. **First-Come, First-Served (FCFS)** - Processes packets in arrival order
2. **Priority Queuing (PQ)** - Processes higher priority packets first
3. **Round-Robin (RR)** - Distributes packets across multiple queues and serves them cyclically

## Features

- **Complete Implementation**: Full Python implementation of three queuing strategies from scratch
- **Packet Simulation**: Realistic packet generation with configurable properties (arrival time, priority, size, service time)
- **Performance Metrics**: Measures latency, throughput, and fairness for each strategy
- **Comprehensive Testing**: Multiple experimental scenarios including high traffic, priority stress tests, and variable service times
- **Visualization**: Detailed graphs and charts comparing strategy performance using matplotlib

## Project Structure

```
.
├── packet.py                # Packet class definition
├── queuing_strategies.py    # Implementation of FCFS, PQ, and RR strategies
├── simulation.py            # Packet generation and simulation framework
├── visualization.py         # Visualization and plotting utilities
├── main.py                  # Main simulation runner with 5 experiments
├── example.py               # Simple example demonstrating basic usage
├── custom_simulation.py     # Interactive/CLI tool for custom simulations
├── test_queuing.py          # Unit tests for all components
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore patterns
└── results/                 # Output directory for generated plots
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

### Custom Experiments

You can create custom experiments by using the provided modules:

```python
from packet import Packet
from queuing_strategies import FCFSQueue, PriorityQueue, RoundRobinQueue
from simulation import PacketGenerator, Simulator, run_experiment
from visualization import plot_all_metrics

# Generate packets
generator = PacketGenerator(seed=42)
packets = generator.generate_packets(
    num_packets=100,
    arrival_rate=2.0,
    priority_distribution={1: 0.5, 2: 0.3, 3: 0.2}
)

# Create strategies
strategies = [
    FCFSQueue(),
    PriorityQueue(),
    RoundRobinQueue(num_queues=3)
]

# Run experiment and visualize
results = run_experiment(packets, strategies)
plot_all_metrics(results, save_path='my_results.png')
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
- **Fairness Index**: Jain's fairness index (higher = more fair distribution)

## Key Findings

From the experimental results:

- **FCFS**: Provides good fairness but cannot prioritize critical traffic
- **Priority Queue**: Efficiently handles high-priority packets but may starve low-priority traffic
- **Round-Robin**: Balances fairness similar to FCFS while distributing load across queues

## Implementation Details

### Packet Class
- Stores packet metadata (id, arrival_time, priority, size, service_time)
- Tracks timing information (start_time, finish_time)
- Calculates latency and waiting time

### Queuing Strategies
- **FCFS**: Uses `collections.deque` for FIFO processing
- **Priority Queue**: Uses `heapq` for priority-based processing
- **Round-Robin**: Maintains multiple queues with cyclic scheduling

### Simulation Framework
- Generates packets with Poisson arrival process
- Supports configurable priority and size distributions
- Event-driven simulation with accurate timing

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
