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

## 2. Problem Statement & Research Goals

### 2.1 Problems to be Explored
This project addresses critical challenges in network packet scheduling:

1.  **Latency vs. Fairness Trade-off**: How to balance low latency for real-time apps while ensuring fair bandwidth for all users.
2.  **Congestion Management**: How different strategies handle buffer overflows (packet dropping) during high traffic bursts.
3.  **Flow Starvation**: Investigating how aggressive flows (large file downloads) can starve small, interactive flows in shared networks.
4.  **Multi-Tenant Isolation**: Evaluating which strategy best isolates users in a shared infrastructure (e.g., cloud/ISP networks).

### 2.2 Research Questions
1.  Which queuing strategy minimizes latency for critical traffic without starving others?
2.  Can **Fair Queueing** effectively protect small flows during severe congestion?
3.  How does **Finite Queue Capacity** impact the performance of FCFS vs. Fair Queue?

---

## 3. Tools & Technologies

We utilize a custom-built Python simulation framework to ensure complete control over the scheduling logic.

| Category | Tool/Library | Purpose |
|----------|--------------|---------|
| **Language** | **Python 3.9+** | Core logic implementation (high readability, rapid prototyping) |
| **Simulation** | **Custom Event-Driven Engine** | Simulates packet arrivals, queuing, processing, and dropping |
| **Data Structure** | `collections.deque`, `heapq` | Efficient implementation of FIFO, Priority, and Fair queues |
| **Visualization** | **Matplotlib** | Generating comparative charts, histograms, and fairness plots |
| **Testing** | **unittest** | Verifying algorithmic correctness (16 automated tests) |

---

## 4. Methodology & Validation

### 4.1 Simulation Methodology
Our approach uses discrete-event simulation to model network behavior:

1.  **Traffic Generation**:
    *   **Bursty Model**: Simulates real-world traffic (web browsing, video) where packets arrive in clusters.
    *   **Poisson Process**: Used as a baseline for random arrivals.
2.  **Queue Simulation**:
    *   Packets are processed by the selected strategy (FCFS, PQ, RR, FQ).
    *   **Finite Buffers**: If the queue is full, the **Dropping Policy** is triggered.
3.  **Data Collection**:
    *   Every packet tracks its `arrival_time`, `start_time`, and `finish_time`.
    *   Dropped packets are recorded for loss analysis.

### 4.2 Validation Strategy
To ensure the accuracy of our results, we employ a rigorous validation process:

*   **Unit Testing**: 16 automated tests verify the logic of each strategy (e.g., ensuring Priority Queue actually serves high-priority first).
*   **Theoretical Verification**: Comparing simulation results with Queuing Theory expectations (e.g., Little's Law).
*   **Extreme Case Testing**:
    *   **Saturation**: Pushing arrival rate > service rate to test stability.
    *   **Starvation**: Sending 90% high-priority traffic to check low-priority handling.

---

## 5. Performance Metrics

We evaluate each strategy using four key quantitative indicators:

| Metric | Definition | Why it matters? |
|--------|------------|-----------------|
| **1. Average Latency** | $T_{finish} - T_{arrival}$ | Critical for real-time apps (VoIP, Gaming). Lower is better. |
| **2. Throughput** | $\frac{Packets_{processed}}{Total\_Time}$ | Measures system efficiency and capacity. Higher is better. |
| **3. Flow Fairness** | Jain's Index: $\frac{(\sum x_i)^2}{n \sum x_i^2}$ | **Crucial for multi-tenant systems.** Measures if all flows get equal service (0-1). |
| **4. Drop Rate** | $\frac{Packets_{dropped}}{Packets_{total}}$ | Indicates reliability during congestion. Lower is better. |

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
