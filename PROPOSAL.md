# QoS Queuing Strategies: A Comparative Analysis
## Fair Queueing Implementation and Performance Evaluation

---

## 1. Executive Summary

This project presents a comprehensive implementation and experimental analysis of **four fundamental Quality of Service (QoS) queuing strategies** for network packet processing. We have successfully implemented and compared:

1. **First-Come, First-Served (FCFS)**
2. **Priority Queuing (PQ)**
3. **Least Attained Service (LAS)**  *Experimental*
4. **Fair Queueing (FQ)**

Our implementation provides a complete simulation framework with **realistic bursty traffic**, **finite queue capacities with packet dropping**, and comprehensive visualization capabilities.

---

## 2. Problem Statement & Research Goals

### 2.1 Exploring LAS and Comparing with Previous Strategies
In previous coursework, we studied fundamental queuing strategies like **FCFS**, **Priority Queue**, and **Fair Queueing**. While these cover basic scheduling needs, they each have limitations in handling diverse traffic patterns, particularly "mice" (short) vs. "elephant" (long) flows.

This project aims to explore **Least Attained Service (LAS)**, a strategy designed to minimize average latency by favoring flows that have received the least service. We will implement LAS and rigorously compare its performance against the standard strategies introduced in the course.

### 2.2 Research Questions
1.  **LAS vs. Fair Queueing**: Can LAS achieve better latency or fairness than the standard Fair Queueing algorithm?
2.  **Impact on "Mice" Flows**: Does LAS effectively prioritize short flows without explicit priority tagging?
3.  **Starvation Risks**: How does LAS handle "elephant" flows under high load compared to Round-Robin?
4.  **Implementation Trade-offs**: Is the complexity of tracking per-flow service justified by the performance gains?

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

## 4. Queuing Strategies Overview

### 4.1 First-Come, First-Served (FCFS)
- **Algorithm**: Process packets in strict arrival order
- **Dropping Policy**: Global Tail Drop
- **Pros**: Simple, predictable
- **Cons**: Poor flow fairness, no prioritization

### 4.2 Priority Queuing (PQ)
- **Algorithm**: Process highest priority packets first
- **Dropping Policy**: Global Tail Drop
- **Pros**: Excellent for latency-sensitive apps
- **Cons**: Starves low-priority traffic

### 4.3 Fair Queueing (FQ)
- **Algorithm**: Per-flow queues with virtual finish time scheduling
- **Dropping Policy**: **Per-Flow Fair Dropping**
- **Pros**: Max-min fairness, perfect isolation
- **Cons**: Complex O(log N) implementation

### 4.4 Least Attained Service (LAS) 🧪 *Experimental*
- **Algorithm**: Serve flow with least total service received
- **Pros**: Minimizes average latency, favors short flows
- **Cons**: Can starve large flows
- **Result**: Performed identically to FQ in bursty traffic scenarios

---

## 5. Methodology & Validation

### 5.1 Simulation Methodology
Our approach uses discrete-event simulation to model network behavior:

1.  **Traffic Generation**:
    *   **Bursty Model**: Simulates real-world traffic (web browsing, video) where packets arrive in clusters.
    *   **Poisson Process**: Used as a baseline for random arrivals.
2.  **Queue Simulation**:
    *   Packets are processed by the selected strategy (FCFS, PQ, RR, FQ, LAS).
    *   **Finite Buffers**: If the queue is full, the **Dropping Policy** is triggered.
3.  **Data Collection**:
    *   Every packet tracks its `arrival_time`, `start_time`, and `finish_time`.
    *   Dropped packets are recorded for loss analysis.

### 5.2 Validation Strategy
To ensure the accuracy of our results, we employ a rigorous validation process:

*   **Unit Testing**: 16 automated tests verify the logic of each strategy (e.g., ensuring Priority Queue actually serves high-priority first).
*   **Theoretical Verification**: Comparing simulation results with Queuing Theory expectations (e.g., Little's Law).
*   **Extreme Case Testing**:
    *   **Saturation**: Pushing arrival rate > service rate to test stability.
    *   **Starvation**: Sending 90% high-priority traffic to check low-priority handling.

---

## 6. Performance Metrics

We evaluate each strategy using four key quantitative### 6.1 Metrics Definition
(See table above)

## 7. Experimental Scenarios

| Experiment | Packets | Arrival Rate | Priority Dist. | Focus |
|------------|---------|--------------|----------------|-------|
| **Basic Comparison** | 100 | 2.0 | 50/30/20 | General performance |
| **High Traffic** | 500 | 5.0 | 60/30/10 | Stress test |
| **Priority Stress** | 200 | 2.5 | 20/30/50 | High-priority handling |
| **Variable Service** | 150 | 2.0 | 40/40/20 | Service time variance |
| **Packet Dropping** | 100 | 5.0 | 60/30/10 | Congestion handling |

### 7.1 Traffic Parameters
- **Arrival Process**: Bursty arrivals (default) or Poisson
- **Priority Levels**: 1 (low), 2 (medium), 3 (high)
- **Packet Sizes**: 500-5000 bytes (configurable distribution)
- **Service Times**: 0.5-2.0 seconds (default)

---

## 8. Preliminary Results

### 8.1 Basic Comparison (Bursty Traffic)

| Strategy | Avg Latency (s) | Throughput (pkt/s) | Flow Fairness |
|----------|-----------------|--------------------|---------------|
| FCFS | 33.17 | 0.76 | 0.789 |
| Priority Queue | 33.02 | 0.76 | 0.742 |
| Round-Robin | 33.12 | 0.76 | 0.785 |
| **Fair Queue**  | 33.52 | 0.76 | **0.932**  |
| **LAS Queue** | 33.52 | 0.76 | **0.932** |

**Key Findings**:
- ✅ **Fair Queue & LAS achieve highest flow fairness (0.932)**
- ✅ FCFS and Round-Robin provide moderate fairness (~0.78)
- ⚠️ Priority Queue sacrifices fairness for priority handling



### 8.2 Packet Dropping Analysis (Congestion)

**Scenario**: 50 packet queue capacity, 100 packets offered
- **FCFS**: 49% drop rate, Flow 2 & 3 completely starved (100% dropped)
- **Fair Queue**: 15% drop rate, all flows protected (balanced dropping)
