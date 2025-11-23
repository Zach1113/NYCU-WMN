# QoS Queuing Strategies: A Comparative Analysis
## Fair Queueing Implementation and Performance Evaluation

**Course**: NYCU Wireless and Mobile Networks  
**Author**: Zach1113  
**Date**: November 2025

---

## 1. Executive Summary

This project presents a comprehensive implementation and experimental analysis of **four fundamental Quality of Service (QoS) queuing strategies** for network packet processing. We have successfully implemented and compared:

1. **First-Come, First-Served (FCFS)**
2. **Priority Queuing (PQ)**
3. **Round-Robin (RR)**
4. **Fair Queueing (FQ)** ⭐ *New Addition*

Our implementation provides a complete simulation framework with **realistic bursty traffic**, **finite queue capacities with packet dropping**, and comprehensive visualization capabilities.

---

## 2. Motivation

### 2.1 Problem Statement
Modern networks must handle diverse traffic types with varying Quality of Service requirements:
- **Real-time applications** (VoIP, video streaming) require low latency
- **Bulk transfers** (file downloads) need high throughput
- **Multi-tenant systems** require fairness across users
- **Congestion** requires intelligent packet dropping policies

### 2.2 Research Questions
1. How do different queuing strategies affect latency, throughput, and fairness?
2. Which strategy performs best under high traffic loads?
3. Can Fair Queueing provide better fairness than traditional approaches?
4. How do strategies handle congestion and packet dropping?

---

## 3. Queuing Strategies Overview

### 3.1 First-Come, First-Served (FCFS)
- **Algorithm**: Process packets in strict arrival order
- **Data Structure**: `collections.deque` (FIFO queue)
- **Dropping Policy**: Global Tail Drop (first flow to arrive hogs buffer)
- **Pros**: Simple, predictable, fair to arrival order
- **Cons**: Cannot prioritize critical traffic, poor flow fairness

### 3.2 Priority Queuing (PQ)
- **Algorithm**: Process highest priority packets first
- **Data Structure**: `heapq` (min-heap)
- **Dropping Policy**: Global Tail Drop
- **Pros**: Excellent for latency-sensitive applications
- **Cons**: May starve low-priority traffic

### 3.3 Round-Robin (RR)
- **Algorithm**: Distribute packets across N queues, serve cyclically
- **Data Structure**: Multiple `deque` queues
- **Dropping Policy**: Global Tail Drop
- **Pros**: Load balancing, prevents starvation
- **Cons**: Does not respect priorities

### 3.4 Fair Queueing (FQ) ⭐
- **Algorithm**: Per-flow queues with virtual finish time scheduling
- **Data Structure**: Dictionary of flow queues + virtual time tracking
- **Dropping Policy**: **Per-Flow Fair Dropping** (partitions buffer among flows)
- **Pros**: Max-min fairness, flow isolation, prevents bandwidth hogging
- **Cons**: More complex implementation

**Key Innovation**: Fair Queueing uses virtual finish times to approximate bit-by-bit round-robin:
```
virtual_start = max(current_virtual_time, flow_last_finish_time)
virtual_finish = virtual_start + service_time
```
The packet with the smallest virtual finish time is processed next.

---

## 4. Implementation Architecture

### 4.1 System Components

```
┌─────────────────────────────────────────────────────────┐
│                   Simulation Framework                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐      ┌─────────────────────────┐    │
│  │   Packet     │──────▶│  Queuing Strategies     │    │
│  │  Generator   │      │  • FCFS                  │    │
│  │              │      │  • Priority Queue        │    │
│  │ • Bursty     │      │  • Round-Robin           │    │
│  │   Traffic    │      │  • Fair Queue ⭐         │    │
│  │ • Priority   │      └─────────────────────────┘    │
│  │   dist.      │                 │                     │
│  └──────────────┘                 ▼                     │
│                          ┌──────────────┐               │
│                          │  Simulator   │               │
│                          │              │               │
│                          │ • Event-     │               │
│                          │   driven     │               │
│                          │ • Metrics    │               │
│                          └──────────────┘               │
│                                 │                        │
│                                 ▼                        │
│                       ┌──────────────────┐              │
│                       │  Visualization   │              │
│                       │                  │              │
│                       │ • Matplotlib     │              │
│                       │ • Comparisons    │              │
│                       │ • Distributions  │              │
│                       └──────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Key Features
- **Realistic Traffic Generation**: Bursty arrival process (simulating video/web traffic)
- **Finite Queue Capacity**: Configurable buffer sizes with packet dropping
- **Comprehensive Metrics**: Latency, throughput, drop rates, flow fairness
- **Extensive Testing**: 16 unit tests with 100% pass rate
- **Professional Visualization**: Multi-panel comparison charts

---

## 5. Experimental Design

### 5.1 Performance Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Average Latency** | `(finish_time - arrival_time)` | Total delay (waiting + service) |
| **Throughput** | `packets_processed / total_time` | Processing rate |
| **Flow Fairness** | `(Σ avg_flow_latency)² / (n × Σ avg_flow_latency²)` | Jain's fairness on flow averages (0-1) |
| **Drop Rate** | `dropped_packets / total_offered` | Percentage of packets dropped |

### 5.2 Experimental Scenarios

| Experiment | Packets | Arrival Rate | Priority Dist. | Focus |
|------------|---------|--------------|----------------|-------|
| **Basic Comparison** | 100 | 2.0 | 50/30/20 | General performance |
| **High Traffic** | 500 | 5.0 | 60/30/10 | Stress test |
| **Priority Stress** | 200 | 2.5 | 20/30/50 | High-priority handling |
| **Variable Service** | 150 | 2.0 | 40/40/20 | Service time variance |
| **Packet Dropping** | 100 | 5.0 | 60/30/10 | Congestion handling |

### 5.3 Traffic Parameters
- **Arrival Process**: Bursty arrivals (default) or Poisson
- **Priority Levels**: 1 (low), 2 (medium), 3 (high)
- **Packet Sizes**: 500-5000 bytes (configurable distribution)
- **Service Times**: 0.5-2.0 seconds (default)

---

## 6. Preliminary Results

### 6.1 Basic Comparison (Bursty Traffic)

| Strategy | Avg Latency (s) | Throughput (pkt/s) | Flow Fairness |
|----------|-----------------|--------------------|---------------|
| FCFS | 33.17 | 0.76 | 0.789 |
| Priority Queue | 33.02 | 0.76 | 0.742 |
| Round-Robin | 33.12 | 0.76 | 0.785 |
| **Fair Queue** ⭐ | 33.52 | 0.76 | **0.932** ✅ |

**Key Findings**:
- ✅ **Fair Queue achieves highest flow fairness (0.932)**
- ✅ FCFS and Round-Robin provide moderate fairness (~0.78)
- ⚠️ Priority Queue sacrifices fairness for priority handling
- ✅ All strategies achieve similar throughput

### 6.2 Packet Dropping Analysis (Congestion)

**Scenario**: 50 packet queue capacity, 100 packets offered
- **FCFS**: 49% drop rate, Flow 2 & 3 completely starved (100% dropped)
- **Fair Queue**: 15% drop rate, all flows protected (balanced dropping)

---

## 7. Technical Implementation Highlights

### 7.1 Fair Queue Algorithm (Pseudocode)

```python
class FairQueue:
    def __init__(self):
        self.flow_queues = {}          # flow_id -> queue
        self.virtual_time = 0.0        # Global virtual time
        self.flow_finish_times = {}    # flow_id -> virtual finish time
    
    def add_packet(self, packet):
        # Per-Flow Fair Dropping Logic
        if queue_is_full:
            per_flow_limit = max_capacity / num_flows
            if len(flow_queue) >= per_flow_limit:
                drop(packet)
                return

        flow_id = get_flow_id(packet)
        flow_queues[flow_id].append(packet)
    
    def process_next(self):
        # Find flow with minimum virtual finish time
        # ... (standard FQ logic)
```

### 7.2 Code Quality Metrics
- **Total Lines of Code**: ~1,800
- **Test Coverage**: 16 unit tests, 100% pass rate
- **Documentation**: Comprehensive docstrings for all classes/methods
- **Design Patterns**: Strategy pattern, Template method

---

## 8. Validation and Testing

### 8.1 Unit Test Results
```
test_fcfs_order ........................... ✅ PASS
test_priority_order ....................... ✅ PASS
test_round_robin_distribution ............. ✅ PASS
test_fair_queue_flow_separation ........... ✅ PASS
test_fair_queue_virtual_time .............. ✅ PASS
test_fair_queue_fairness .................. ✅ PASS
test_fair_queue_empty ..................... ✅ PASS
test_metrics_calculation .................. ✅ PASS

Ran 16 tests in 0.001s - ALL PASSED ✅
```

---

## 9. Expected Outcomes

### 9.1 Performance Predictions

**Under High Traffic Load**:
- Fair Queue should maintain better fairness than Priority Queue
- FCFS may show increased latency variance

**Under Congestion (Packet Dropping)**:
- Fair Queue will protect small flows from starvation
- FCFS will allow aggressive flows to hog the buffer

### 9.2 Visualization Outputs

The simulation generates:
1. **4-panel performance dashboard** (latency, waiting time, throughput, flow fairness)
2. **Latency distribution histograms** for each strategy
3. **Priority-based fairness analysis**
4. **Comparative bar charts**

---

## 10. Real-World Applications

### 10.1 Use Cases by Strategy

| Strategy | Best For | Example Applications |
|----------|----------|---------------------|
| **FCFS** | Simple, non-critical traffic | Email servers, batch processing |
| **Priority Queue** | Latency-sensitive apps | VoIP, video conferencing, gaming |
| **Round-Robin** | Load balancing | Multi-core scheduling, web servers |
| **Fair Queue** | Multi-tenant systems | ISP networks, cloud platforms, shared infrastructure |

### 10.2 Industry Relevance
- **Cisco IOS**: Uses Weighted Fair Queueing (WFQ)
- **Linux Traffic Control**: Implements Stochastic Fair Queueing (SFQ)
- **Data Centers**: Use variants for tenant isolation
- **5G Networks**: QoS mechanisms based on these principles

---

## 11. Conclusions

### 11.1 Key Achievements
✅ Successfully implemented 4 queuing strategies from scratch  
✅ **Fair Queue shows superior flow fairness (0.932)**  
✅ Implemented **realistic packet dropping** with finite queues  
✅ Comprehensive testing framework with 100% test pass rate  
✅ Professional visualization and analysis tools  

### 11.2 Key Insights
1. **Fair Queue provides best protection** for flows during congestion
2. **Priority Queue excels for latency** but sacrifices fairness
3. **FCFS** suffers from "tail drop" issues under heavy load
4. **Trade-offs exist** between complexity and fairness

---

## 12. Future Work

### 12.1 Potential Extensions
1. **Weighted Fair Queueing (WFQ)**: Add per-flow weights
2. **Deficit Round-Robin (DRR)**: Improve Round-Robin with deficit counters
3. **Class-Based Queueing (CBQ)**: Hierarchical bandwidth allocation
4. **Token Bucket Shaping**: Add traffic shaping mechanisms

### 12.2 Advanced Features
- **Active Queue Management**: RED, WRED (vs current Tail Drop)
- **Preemption**: Allow packet preemption for ultra-low latency
- **Multi-server queues**: Parallel processing simulation
- **Network topology**: Simulate multiple routers/switches

---

## 13. References

### 13.1 Academic Papers
1. Demers, A., Keshav, S., & Shenker, S. (1989). "Analysis and Simulation of a Fair Queueing Algorithm." *ACM SIGCOMM*.
2. Nagle, J. (1987). "On Packet Switches with Infinite Storage." *IEEE Transactions on Communications*.
3. Jain, R., Chiu, D., & Hawe, W. (1984). "A Quantitative Measure of Fairness and Discrimination for Resource Allocation in Shared Computer Systems."

### 13.2 Technical Resources
- RFC 2474: Definition of the Differentiated Services Field (DS Field)
- RFC 2475: An Architecture for Differentiated Services
- Cisco QoS Documentation: Quality of Service Networking

### 13.3 Implementation
- Python 3.7+ with matplotlib and numpy
- Source code: [github.com/Zach1113/NYCU-WMN](https://github.com/Zach1113/NYCU-WMN)

---

## 14. Appendix

### 14.1 How to Run

```bash
# Setup (one-time)
cd NYCU-WMN
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run experiments
python example.py          # Quick demo
python main.py            # Full experiments (5 scenarios)
python custom_simulation.py  # Interactive mode

# Run tests
python test_queuing.py

# Deactivate when done
deactivate
```

### 14.2 Project Structure
```
NYCU-WMN/
├── packet.py                 # Packet class (79 lines)
├── queuing_strategies.py     # All 4 strategies (320 lines)
├── simulation.py             # Simulation framework (165 lines)
├── visualization.py          # Plotting utilities (204 lines)
├── main.py                   # Experiment runner (232 lines)
├── example.py                # Simple demo (66 lines)
├── custom_simulation.py      # Interactive tool (146 lines)
├── test_queuing.py          # Unit tests (287 lines)
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
└── results/                  # Generated visualizations
```

### 14.3 System Requirements
- **Python**: 3.7 or higher
- **Dependencies**: matplotlib ≥ 3.5.0, numpy ≥ 1.21.0
- **OS**: macOS, Linux, Windows
- **Memory**: ~100 MB for typical experiments

---

## 15. Contact & Acknowledgments

**Author**: Zach1113  
**Course**: NYCU Wireless and Mobile Networks  
**Repository**: [github.com/Zach1113/NYCU-WMN](https://github.com/Zach1113/NYCU-WMN)

**Acknowledgments**:
- This implementation is based on standard queueing theory and network QoS principles
- Fair Queueing algorithm inspired by Demers, Keshav, and Shenker (1989)
- Developed for educational purposes at National Yang Ming Chiao Tung University

---

**Document Version**: 1.0  
**Last Updated**: November 22, 2025  
**Status**: ✅ Implementation Complete & Tested
