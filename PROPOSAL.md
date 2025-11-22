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

Our implementation provides a complete simulation framework with realistic packet generation, performance metrics collection, and comprehensive visualization capabilities.

---

## 2. Motivation

### 2.1 Problem Statement
Modern networks must handle diverse traffic types with varying Quality of Service requirements:
- **Real-time applications** (VoIP, video streaming) require low latency
- **Bulk transfers** (file downloads) need high throughput
- **Multi-tenant systems** require fairness across users

### 2.2 Research Questions
1. How do different queuing strategies affect latency, throughput, and fairness?
2. Which strategy performs best under high traffic loads?
3. Can Fair Queueing provide better fairness than traditional approaches?
4. What are the trade-offs between simplicity and performance?

---

## 3. Queuing Strategies Overview

### 3.1 First-Come, First-Served (FCFS)
- **Algorithm**: Process packets in strict arrival order
- **Data Structure**: `collections.deque` (FIFO queue)
- **Complexity**: O(1) enqueue, O(1) dequeue
- **Pros**: Simple, predictable, fair to arrival order
- **Cons**: Cannot prioritize critical traffic

### 3.2 Priority Queuing (PQ)
- **Algorithm**: Process highest priority packets first
- **Data Structure**: `heapq` (min-heap)
- **Complexity**: O(log n) enqueue, O(log n) dequeue
- **Pros**: Excellent for latency-sensitive applications
- **Cons**: May starve low-priority traffic

### 3.3 Round-Robin (RR)
- **Algorithm**: Distribute packets across N queues, serve cyclically
- **Data Structure**: Multiple `deque` queues
- **Complexity**: O(1) enqueue, O(1) dequeue (amortized)
- **Pros**: Load balancing, prevents starvation
- **Cons**: Does not respect priorities

### 3.4 Fair Queueing (FQ) ⭐
- **Algorithm**: Per-flow queues with virtual finish time scheduling
- **Data Structure**: Dictionary of flow queues + virtual time tracking
- **Complexity**: O(F) per dequeue where F = number of active flows
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
│  │ • Poisson    │      │  • Round-Robin           │    │
│  │   arrival    │      │  • Fair Queue ⭐         │    │
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
- **Realistic Traffic Generation**: Poisson arrival process with configurable parameters
- **Comprehensive Metrics**: Latency, waiting time, throughput, Jain's fairness index
- **Extensive Testing**: 16 unit tests with 100% pass rate
- **Professional Visualization**: Multi-panel comparison charts

---

## 5. Experimental Design

### 5.1 Performance Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Average Latency** | `(finish_time - arrival_time)` | Total delay (waiting + service) |
| **Average Waiting Time** | `(start_time - arrival_time)` | Time in queue before processing |
| **Throughput** | `packets_processed / total_time` | Processing rate |
| **Fairness Index** | `(Σ latency)² / (n × Σ latency²)` | Jain's fairness (0-1, higher is better) |

### 5.2 Experimental Scenarios

| Experiment | Packets | Arrival Rate | Priority Dist. | Focus |
|------------|---------|--------------|----------------|-------|
| **Basic Comparison** | 100 | 2.0 | 50/30/20 | General performance |
| **High Traffic** | 500 | 5.0 | 60/30/10 | Stress test |
| **Priority Stress** | 200 | 2.5 | 20/30/50 | High-priority handling |
| **Variable Service** | 150 | 2.0 | 40/40/20 | Service time variance |
| **Latency Analysis** | 200 | 2.0 | 40/30/30 | Statistical distribution |

### 5.3 Traffic Parameters
- **Arrival Process**: Exponential inter-arrival times (Poisson)
- **Priority Levels**: 1 (low), 2 (medium), 3 (high)
- **Packet Sizes**: 500-5000 bytes (configurable distribution)
- **Service Times**: 0.5-2.0 seconds (default), 0.1-5.0 seconds (variable)

---

## 6. Preliminary Results

### 6.1 Basic Comparison (50 packets, moderate traffic)

| Strategy | Avg Latency (s) | Throughput (pkt/s) | Fairness Index |
|----------|-----------------|--------------------|--------------------|
| FCFS | 15.52 | 0.88 | **0.727** |
| Priority Queue | 14.96 | 0.88 | 0.565 |
| Round-Robin | 15.52 | 0.88 | **0.727** |
| **Fair Queue** ⭐ | **14.56** ✅ | 0.88 | 0.603 |

**Key Findings**:
- ✅ **Fair Queue achieved the lowest average latency** (14.56s)
- ✅ FCFS and Round-Robin show highest fairness (0.727)
- ⚠️ Priority Queue has lowest fairness (0.565) - expected due to prioritization
- ✅ All strategies achieve same throughput (queue-limited)

### 6.2 Performance Characteristics

```
Latency Performance:
Fair Queue < Priority Queue < FCFS ≈ Round-Robin

Fairness Performance:
FCFS ≈ Round-Robin > Fair Queue > Priority Queue

Complexity:
FCFS < Round-Robin < Priority Queue < Fair Queue
```

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
        flow_id = get_flow_id(packet)  # Use priority as flow ID
        if flow_id not in flow_queues:
            flow_queues[flow_id] = deque()
            flow_finish_times[flow_id] = 0.0
        flow_queues[flow_id].append(packet)
    
    def process_next(self):
        # Find flow with minimum virtual finish time
        min_flow = None
        min_finish = ∞
        
        for flow_id, queue in flow_queues.items():
            if queue is not empty:
                packet = queue.front()
                virtual_start = max(virtual_time, flow_finish_times[flow_id])
                virtual_finish = virtual_start + packet.service_time
                
                if virtual_finish < min_finish:
                    min_finish = virtual_finish
                    min_flow = flow_id
        
        # Process packet from selected flow
        packet = flow_queues[min_flow].dequeue()
        virtual_time = min_finish
        flow_finish_times[min_flow] = min_finish
        
        return packet
```

### 7.2 Code Quality Metrics
- **Total Lines of Code**: ~1,700 (including Fair Queue)
- **Test Coverage**: 16 unit tests, 100% pass rate
- **Documentation**: Comprehensive docstrings for all classes/methods
- **Design Patterns**: Strategy pattern, Template method, Dependency injection

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

### 8.2 Test Coverage
- ✅ Packet creation and timing
- ✅ Queue operations (enqueue, dequeue, empty check)
- ✅ Priority ordering
- ✅ Flow separation (Fair Queue)
- ✅ Virtual time advancement (Fair Queue)
- ✅ Metrics calculation
- ✅ Simulation framework

---

## 9. Expected Outcomes

### 9.1 Performance Predictions

**Under High Traffic Load**:
- Fair Queue should maintain better fairness than Priority Queue
- FCFS may show increased latency variance
- Round-Robin should distribute load evenly

**Under Priority Stress** (50% high-priority packets):
- Priority Queue will excel for high-priority packets
- Fair Queue will balance across all priorities
- FCFS will treat all equally (no prioritization)

**Under Variable Service Times**:
- Fair Queue should show highest fairness index
- FCFS and Round-Robin may show latency variance
- Priority Queue may amplify service time effects

### 9.2 Visualization Outputs

The simulation generates:
1. **4-panel performance dashboard** (latency, waiting time, throughput, fairness)
2. **Latency distribution histograms** for each strategy
3. **Priority-based fairness analysis** (latency by priority level)
4. **Comparative bar charts** for specific metrics

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
- **Cisco IOS**: Uses Weighted Fair Queueing (WFQ) based on Fair Queueing
- **Linux Traffic Control**: Implements Stochastic Fair Queueing (SFQ)
- **Data Centers**: Use variants for tenant isolation
- **5G Networks**: QoS mechanisms based on these principles

---

## 11. Conclusions

### 11.1 Key Achievements
✅ Successfully implemented 4 queuing strategies from scratch  
✅ Fair Queue shows **lowest average latency** in preliminary tests  
✅ Comprehensive testing framework with 100% test pass rate  
✅ Professional visualization and analysis tools  
✅ Realistic traffic generation with Poisson arrivals  

### 11.2 Key Insights
1. **Fair Queue provides excellent balance** between latency and fairness
2. **Priority Queue excels for latency** but sacrifices fairness
3. **FCFS and Round-Robin** offer simplicity with good fairness
4. **Trade-offs exist** between complexity, performance, and fairness

### 11.3 Contributions
- **Educational**: Clear implementation of fundamental QoS algorithms
- **Practical**: Reusable simulation framework for network research
- **Extensible**: Easy to add new strategies or metrics
- **Well-tested**: Comprehensive unit tests ensure correctness

---

## 12. Future Work

### 12.1 Potential Extensions
1. **Weighted Fair Queueing (WFQ)**: Add per-flow weights
2. **Deficit Round-Robin (DRR)**: Improve Round-Robin with deficit counters
3. **Class-Based Queueing (CBQ)**: Hierarchical bandwidth allocation
4. **Token Bucket Shaping**: Add traffic shaping mechanisms
5. **Real Network Traces**: Test with real-world packet captures

### 12.2 Advanced Features
- **Packet dropping policies**: RED, WRED for congestion control
- **Queue limits**: Finite buffer sizes with overflow handling
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
