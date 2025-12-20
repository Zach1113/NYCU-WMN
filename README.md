# QoS Queuing Strategies Simulation

A comprehensive implementation and experimental analysis of Quality of Service (QoS) queuing strategies for network packet processing with **realistic bursty traffic patterns**.

## Overview

This project explores **Least Attained Service (LAS)** queuing and compares it with other QoS strategies:

1. **First-Come, First-Served (FCFS)** - Processes packets in arrival order
2. **Fair Queueing (FQ)** - Maintains per-flow queues with virtual finish times for fairness
3. **Least Attained Service (LAS)** - Serves the flow with least cumulative service (from OS scheduling theory)

## Features

- **LAS Implementation**: Novel implementation of Least Attained Service scheduling for network packets
- **Realistic Traffic Scenarios**: 5 scenarios including Message Texting, Video Streaming, Online Meeting, File Download, and Mice & Elephants
- **Finite Queue Capacity**: Support for limited buffer sizes with packet dropping
- **Throughput-Based Fairness**: Measures flow fairness including starved flows
- **Performance Metrics**: Measures latency, throughput, fairness, and drop rates
- **Comprehensive Report**: Detailed experiment report following academic structure

## Project Structure

```
.
├── packet.py                    # Packet class definition
├── queuing_strategies.py        # Implementation of FCFS, FQ, and LAS
├── simulation.py                # Packet generation and simulation framework
├── visualization.py             # Visualization and plotting utilities
├── main.py                      # Main simulation runner
├── demo_packet_dropping.py      # Packet dropping demonstration
├── demo_realistic_scenarios.py  # 5 realistic traffic scenarios
├── EXPERIMENT_REPORT.md         # Complete experiment report
├── README.md                    # This file
├── test_queuing.py              # Unit tests
├── requirements.txt             # Python dependencies
└── results/                     # Output directory for generated plots
```

## Installation

```bash
git clone https://github.com/Zach1113/NYCU-WMN.git
cd NYCU-WMN
pip install -r requirements.txt
```

## Quick Start

### Run Realistic Scenarios Demo
```bash
python3 demo_realistic_scenarios.py
```

This runs 5 traffic scenarios comparing FCFS, Fair Queue, and LAS Queue.

### Run Packet Dropping Demo
```bash
python3 demo_packet_dropping.py
```

### Run Main Experiments
```bash
python3 main.py
```

## Key Results

### Flow Fairness Comparison

| Scenario | FCFS | Fair Queue | LAS Queue | Winner |
|----------|------|------------|-----------|--------|
| Message Texting | 1.0000 | 1.0000 | 1.0000 | Tie |
| Video Streaming | **0.9982** | 0.8583 | 0.9231 | FCFS |
| Online Meeting | 0.9974 | **0.9996** | 0.9191 | FQ |
| File Download | **0.9865** | 0.8354 | 0.8673 | FCFS |
| Mice & Elephants | 0.4846 | 0.9421 | **0.9443** | LAS |

### LAS Achieves Most Balanced Performance

| Metric | FCFS | Fair Queue | LAS Queue |
|--------|------|------------|-----------|
| **Average Fairness** | 0.8933 | 0.9271 | **0.9308** |
| **Std Deviation** | 0.2044 | 0.0692 | **0.0429** |
| **Minimum Score** | 0.4846 | 0.8354 | **0.8673** |

**LAS Queue provides the most consistent and reliable performance across all scenarios.**

### LAS: Better Results with Simpler Implementation

| Aspect | Fair Queue | LAS Queue |
|--------|------------|-----------|
| Lines of Code | 46 lines | 27 lines |
| State Tracking | Virtual time + finish times | Only service counter |
| Prediction Required | Must predict virtual finish time | No prediction needed |

## Understanding LAS (Least Attained Service)

LAS originated from **operating systems CPU scheduling** (also known as Foreground-Background scheduling):

> **Core Principle**: "Always serve the flow that has received the least amount of service so far."

**Advantages:**
- Optimal for unknown job/flow sizes
- Favors short flows naturally (no explicit priority needed)
- Simpler than Fair Queueing (no virtual time calculation)
- More feasible for real-world implementation

## Strategy Selection Guidelines

| Use Case | Recommended Strategy |
|----------|---------------------|
| Simple, low-priority traffic | FCFS |
| Equal real-time flows (VoIP, meetings) | Fair Queue |
| Mixed mice/elephant flows | **LAS Queue** |
| Resource-constrained devices | **LAS Queue** |
| Unknown traffic patterns | **LAS Queue** |

## Performance Metrics

- **Average Latency**: Total delay from arrival to completion
- **Average Waiting Time**: Time spent waiting in queue
- **Throughput**: Packets processed per unit time
- **Drop Rate**: Percentage of packets dropped
- **Flow Fairness**: Jain's fairness index on throughput ratios (includes starved flows)

## Requirements

- Python 3.7+
- matplotlib >= 3.5.0
- numpy >= 1.21.0

## Documentation

See [EXPERIMENT_REPORT.md](EXPERIMENT_REPORT.md) for the complete experiment report including:
- System model and network environment
- Algorithm implementations
- Detailed results for all 5 scenarios
- Conclusions and strategy recommendations

## License

This project is developed for educational purposes as part of NYCU Wireless and Mobile Networks coursework.

## Author

Zach1113
