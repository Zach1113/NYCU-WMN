# Least Attained Service (LAS) Queueing: A Comparative Study with Other QoS Strategies

---

## 1. 主題 (Topic)

### Research Title
**Exploring Least Attained Service (LAS) Queueing and Comparing with Other QoS Strategies**

### Research Objective
This project explores the **Least Attained Service (LAS)** queueing strategy and compares its performance against QoS strategies taught in previous courses:
- **FCFS (First-Come, First-Served)**
- **Fair Queueing (FQ)**

### Research Questions
1. Can LAS achieve better latency or fairness than other Fair Queueing?
2. Does LAS effectively prioritize short flows without explicit priority tagging?
3. How do different strategies handle packet dropping under congestion?
4. In what scenarios does each strategy perform best?

### Introduction to LAS (Least Attained Service)

**Least Attained Service (LAS)**, also known as **Foreground-Background (FB)** scheduling, is a scheduling algorithm that originated in **operating systems theory**. The algorithm was developed to optimize system performance, particularly minimizing mean response time, without requiring prior knowledge of job sizes.

#### Historical Background

| Aspect | Description |
|--------|-------------|
| **Origin** | Operating Systems CPU scheduling |
| **Also Known As** | Foreground-Background (FB), Generalized FB |
| **First Applications** | Process scheduling in time-sharing systems |
| **Later Adoption** | Network packet/flow scheduling |

#### Core Principle

The fundamental idea of LAS is simple yet powerful:

> **"Always serve the job (or flow) that has received the least amount of service so far."**

This approach has several theoretical advantages:
- **Optimal for unknown job sizes**: Unlike Shortest Job First (SJF) or Shortest Remaining Processing Time (SRPT), LAS does not require knowing or estimating job lengths in advance
- **Favors short jobs naturally**: New arrivals and small jobs get immediate priority
- **Preemptive**: A newly arriving job can preempt the current job if it has received less service

#### From OS to Networks

LAS has been successfully adapted from operating systems to network scheduling:

| Domain | Application |
|--------|-------------|
| **Operating Systems** | CPU scheduling for processes with unknown execution times |
| **Network Routers** | Packet scheduling to reduce average flow completion time |
| **Web Servers** | Request scheduling to improve response time for short requests |
| **Data Centers** | Flow scheduling to protect "mice" flows from "elephant" flows |

In network scheduling, LAS treats each **flow** (identified by source/destination) as a "job" and tracks the cumulative bytes or service time each flow has received. This makes it particularly effective for scenarios where small, interactive flows (web browsing, API calls) compete with large bulk transfers (file downloads, backups).

---

## 2. 系統/網路拓樸或環境 (System Model / Network Environment)

### Simulation Environment

```
┌─────────────────────────────────────────────────────────────┐
│                    Network Simulation Model                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────────┐                                          │
│   │   Traffic    │      ┌─────────────────────────┐         │
│   │  Generator   │─────▶│   Queueing Strategy     │         │
│   │              │      │   (FCFS / FQ / LAS)     │         │
│   │ • Bursty     │      │                         │         │
│   │ • Realistic  │      │   ┌─────────────────┐   │         │
│   │ • Multi-flow │      │   │  Finite Buffer  │   │         │
│   └──────────────┘      │   │  (Packet Drop)  │   │         │
│                         │   └─────────────────┘   │         │
│                         └─────────────────────────┘         │
│                                    │                        │
│                                    ▼                        │
│                         ┌─────────────────────┐             │
│                         │  Performance        │             │
│                         │  Metrics Collection │             │
│                         └─────────────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

### System Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Language** | Python 3.9+ | Simulation implementation |
| **Queue Capacity** | 15-30 packets | Finite buffer (causes dropping) |
| **Traffic Model** | Bursty | Realistic traffic patterns |
| **Number of Flows** | 2-12 | Depending on scenario |
| **Packet Size** | 100-5000 bytes | Variable sizes |
| **Service Time** | 0.01-0.6 seconds | Processing time per packet |

### Traffic Scenarios

We designed **5 traffic scenarios** to evaluate the strategies:

| Scenario | Description | Flows | Characteristics |
|----------|-------------|-------|-----------------|
| **Message Texting** | 3 users sending messages | 3 equal | Small packets, bursty |
| **Video Streaming** | HD + SD video streams | 2 unequal | Large chunks, continuous |
| **Online Meeting** | 3 participants (audio+video) | 3 equal | Real-time, mixed sizes |
| **File Download** | 1 download + 2 background | 3 unequal | Aggressive elephant flow |
| **Mice & Elephants** | 2 downloads + 10 web requests | 12 mixed | Tests LAS advantage |

---

## 3. 方法 (Approach / Method / Algorithm)

### 3.1 FCFS (First-Come, First-Served)

**Algorithm:**
```
Queue: Single FIFO queue

add_packet(packet):
    if queue is full:
        DROP packet  # Tail drop
    else:
        queue.append(packet)

process_next():
    return queue.pop_front()  # First in, first out
```

**Characteristics:**
- Simple implementation (O(1))
- No flow isolation
- Aggressive flows can starve others

---

### 3.2 Fair Queueing (FQ)

**Algorithm:**
```
Queue: Separate queue per flow + virtual finish times

add_packet(packet):
    flow_id = get_flow(packet)
    
    # Per-flow fair dropping
    if total_queue_size >= max_capacity:
        per_flow_limit = max_capacity / num_flows
        if flow_queue[flow_id].size >= per_flow_limit:
            DROP packet
            return
    
    flow_queue[flow_id].append(packet)

process_next():
    # Serve flow with smallest virtual finish time
    min_flow = argmin(virtual_finish_time[f] for all flows f)
    packet = flow_queue[min_flow].pop_front()
    virtual_finish_time[min_flow] += packet.service_time
    return packet
```

**Characteristics:**
- Perfect flow isolation
- Per-flow fair dropping
- More complex (O(F) where F = flows)

---

### 3.3 LAS (Least Attained Service)

**Algorithm:**
```
Queue: Separate queue per flow + service counter

add_packet(packet):
    flow_id = get_flow(packet)
    
    # Drop from flow with MOST service (protect small flows)
    if total_queue_size >= max_capacity:
        max_service_flow = argmax(service_received[f])
        DROP packet from max_service_flow
    
    flow_queue[flow_id].append(packet)

process_next():
    # Serve flow with LEAST total service received
    min_flow = argmin(service_received[f] for all flows f)
    packet = flow_queue[min_flow].pop_front()
    service_received[min_flow] += packet.service_time
    return packet
```

**Characteristics:**
- Automatically prioritizes new/small flows
- No need for explicit priority tagging
- Simpler than FQ (no virtual time)
- May starve large flows continuously

---

### 3.4 Flow Fairness Metric

We use **Jain's Fairness Index** based on throughput:

$$
\text{Fairness} = \frac{(\sum_{i=1}^{n} x_i)^2}{n \cdot \sum_{i=1}^{n} x_i^2}
$$

Where $x_i = \frac{\text{packets processed for flow } i}{\text{packets offered for flow } i}$

- **1.0** = Perfect fairness (all flows get equal throughput ratio)
- **1/n** = Worst case (only one flow gets service)

---

## 4. 效能測試或驗證 (Performance Evaluation & Results)

### 4.1 Experiment Results Summary

| Scenario | Queue | FCFS | Fair Queue | LAS Queue | Winner |
|----------|-------|------|------------|-----------|--------|
| Message Texting | 15 | 1.0000 | 1.0000 | 1.0000 | Tie |
| Video Streaming | 25 | **0.9982** | 0.8583 | 0.9231 | FCFS |
| Online Meeting | 30 | 0.9974 | **0.9996** | 0.9191 | FQ |
| File Download | 20 | **0.9865** | 0.8354 | 0.8673 | FCFS |
| Mice & Elephants | 25 | 0.4846 | 0.9421 | **0.9443** | LAS |

---

### 4.2 Detailed Results by Scenario

#### Scenario 1: Message Texting

**Configuration:**
- 3 users, ~28 packets total
- Small packets (100-500 bytes)
- Queue capacity: 15

**Results:**
| Strategy | Processed | Dropped | Drop Rate | Fairness |
|----------|-----------|---------|-----------|----------|
| FCFS | 28 | 0 | 0.0% | 1.0000 |
| Fair Queue | 28 | 0 | 0.0% | 1.0000 |
| LAS Queue | 28 | 0 | 0.0% | 1.0000 |

**Observation:** No congestion, all strategies perform equally.

---

#### Scenario 2: Video Streaming

**Configuration:**
- 2 streams: HD (50 packets) + SD (30 packets)
- Large video chunks
- Queue capacity: 25

**Results:**
| Strategy | Processed | Dropped | Drop Rate | Fairness |
|----------|-----------|---------|-----------|----------|
| FCFS | 43 | 37 | 46.2% | **0.9982** |
| Fair Queue | 46 | 34 | 42.5% | 0.8583 |
| LAS Queue | 48 | 32 | 40.0% | 0.9231 |

**Drop Distribution:**
| Strategy | HD Stream (Flow 1) | SD Stream (Flow 2) |
|----------|-------------------|-------------------|
| FCFS | 48.0% dropped | 43.3% dropped |
| Fair Queue | 62.0% dropped | 10.0% dropped |
| LAS Queue | 54.0% dropped | 16.7% dropped |

**Observation:** FCFS drops proportionally; FQ/LAS protect the smaller SD stream.

---

#### Scenario 3: Online Meeting

**Configuration:**
- 3 participants, 45 packets each (135 total)
- Audio + Video mix
- Queue capacity: 30

**Results:**
| Strategy | Processed | Dropped | Drop Rate | Fairness |
|----------|-----------|---------|-----------|----------|
| FCFS | 74 | 61 | 45.2% | 0.9974 |
| Fair Queue | 74 | 61 | 45.2% | **0.9996** |
| LAS Queue | 72 | 63 | 46.7% | 0.9191 |

**Observation:** Fair Queue achieves near-perfect fairness for equal flows.

---

#### Scenario 4: File Download

**Configuration:**
- 1 large download (60 packets) + 2 background tasks (15+10 packets)
- Queue capacity: 20

**Results:**
| Strategy | Processed | Dropped | Drop Rate | Fairness |
|----------|-----------|---------|-----------|----------|
| FCFS | 31 | 54 | 63.5% | 0.9865 |
| Fair Queue | 42 | 43 | 50.6% | 0.8354 |
| LAS Queue | 46 | 39 | 45.9% | 0.8673 |

**Drop Distribution:**
| Strategy | Download (Flow 1) | Background 1 | Background 2 |
|----------|-------------------|--------------|--------------|
| FCFS | 63.3% dropped | 60.0% dropped | 70.0% dropped |
| Fair Queue | 71.7% dropped | **0% dropped** | **0% dropped** |
| LAS Queue | 65.0% dropped | **0% dropped** | **0% dropped** |

**Observation:** FQ and LAS completely protect background flows!

---

#### Scenario 5: Mice and Elephants (LAS Advantage)

**Configuration:**
- 2 elephant flows (40+35 packets) - large downloads
- 10 mice flows (2-4 packets each) - web requests
- Queue capacity: 25

**Results:**
| Strategy | Processed | Dropped | Drop Rate | Fairness |
|----------|-----------|---------|-----------|----------|
| FCFS | 37 | 68 | 64.8% | 0.4846 |
| Fair Queue | 60 | 45 | 42.9% | 0.9421 |
| LAS Queue | 61 | 44 | 41.9% | **0.9443** |

**Drop Distribution (Mice Flows 3-12):**
| Strategy | Mice Protected? | Mice Drop Rate |
|----------|-----------------|----------------|
| FCFS | No | 25-100% per mouse |
| Fair Queue | Yes | **0% for all mice** |
| LAS Queue | Yes | **0% for all mice** |

**Observation:** LAS achieves the highest fairness by prioritizing least-served flows (mice).

---

### 4.3 Visual Comparison

```
Flow Fairness by Scenario
═══════════════════════════════════════════════════════════════

 Message Texting      ████████████████████████████████████ 1.00 (All)

 Video Streaming      FCFS: ████████████████████████████████ 0.998 ★
                      FQ:   ██████████████████████████       0.858
                      LAS:  ██████████████████████████████   0.923

 Online Meeting       FCFS: ███████████████████████████████  0.997
                      FQ:   ████████████████████████████████ 1.000 ★
                      LAS:  ██████████████████████████████   0.919

 File Download        FCFS: ███████████████████████████████  0.987 ★
                      FQ:   ██████████████████████████       0.835
                      LAS:  ███████████████████████████      0.867

 Mice/Elephants       FCFS: ███████████████                  0.485
                      FQ:   ██████████████████████████████   0.942
                      LAS:  ██████████████████████████████   0.944 ★
```

---

## 5. 結論 (Conclusions)

### 5.1 LAS Achieves Most Balanced Performance

Analyzing the fairness scores across all five scenarios:

| Metric | FCFS | Fair Queue | LAS Queue |
|--------|------|------------|-----------|
| **Average Fairness** | 0.8933 | 0.9271 | **0.9308** |
| **Standard Deviation** | 0.2044 | 0.0692 | **0.0429** |
| **Minimum Score** | 0.4846 | 0.8354 | **0.8673** |
| **Maximum Score** | 1.0000 | 1.0000 | 1.0000 |

**LAS Queue demonstrates:**
- **Highest average fairness** (0.9308) across all scenarios
- **Lowest standard deviation** (0.0429) - most consistent performance
- **Highest minimum score** (0.8673) - never performs extremely poorly

This means LAS provides the most **reliable and predictable** performance regardless of traffic pattern.

---

### 5.2 LAS: Better Results with Simpler Implementation

| Aspect | Fair Queue (FQ) | LAS Queue |
|--------|-----------------|-----------|
| **Lines of Code** | 46 lines | 27 lines |
| **State Tracking** | Virtual time + finish times | Only service counter |
| **Complexity** | O(F) with virtual time sync | O(F) simple comparison |
| **Prediction Required** | Must predict virtual finish time | No prediction needed |

**Key Implementation Advantages of LAS:**

1. **No Virtual Time Calculation**: FQ requires maintaining and synchronizing virtual finish times across flows, which adds complexity. LAS simply tracks "how much service has each flow received" - a straightforward counter.

2. **More Feasible in Real-World**: 
   - LAS does not require predicting when a packet will finish processing
   - Only requires tracking cumulative service time (easily measured)
   - Easier to implement in hardware (simple comparator)

3. **Simpler Debugging**: With LAS, the scheduling decision is intuitive - "serve whoever has gotten the least service so far." FQ's virtual time concept is more abstract and harder to debug.

---

### 5.3 Key Findings Summary

1. **LAS vs FQ Equivalence**: Under continuous backlog, LAS and FQ make equivalent scheduling decisions through different mechanisms:
   - FQ: Tracks virtual finish times (complex)
   - LAS: Tracks total service received (simple)

2. **LAS Advantage**: In mixed "Mice and Elephants" scenarios:
   - LAS achieves **highest fairness (0.9443)**
   - LAS **completely protects all small flows** (0% drop rate)
   - LAS requires **40% less code** than FQ

3. **FCFS Limitations**: Under congestion with aggressive flows:
   - FCFS can completely **starve small flows**
   - Fairness drops to **0.33-0.48** in worst cases

4. **Flow Protection**: Both FQ and LAS provide **flow isolation** that FCFS lacks

---

### 5.4 Strategy Selection Guidelines

| Use Case | Recommended Strategy | Reason |
|----------|---------------------|--------|
| Simple, low-priority traffic | **FCFS** | Simplest, no overhead |
| Equal real-time flows (VoIP, meetings) | **Fair Queue** | Best for symmetric traffic |
| Mixed mice/elephant flows (web + downloads) | **LAS Queue** | Protects small flows automatically |
| Multi-tenant systems | **FQ or LAS** | Flow isolation required |
| **Resource-constrained devices** | **LAS Queue** | Simpler implementation |
| **Unknown traffic patterns** | **LAS Queue** | Most balanced performance |

### 5.5 Future Work

1. **Weighted LAS**: Add per-flow weights for differentiated service
2. **Active Queue Management**: Integrate RED/CoDel for proactive dropping
3. **Real-world validation**: Test with actual network traces
4. **Latency analysis**: Compare end-to-end delay characteristics

---

**Project Repository:** [github.com/Zach1113/NYCU-WMN](https://github.com/Zach1113/NYCU-WMN)
