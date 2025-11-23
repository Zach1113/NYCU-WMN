"""
Queuing strategies for Quality of Service (QoS) simulation.
"""

import heapq
from collections import deque
from packet import Packet


class QueueingStrategy:
    """Base class for queuing strategies."""
    
    def __init__(self, name, max_queue_size=None):
        """
        Initialize the queuing strategy.
        
        Args:
            name: Name of the strategy
            max_queue_size: Maximum queue size (None = infinite)
        """
        self.name = name
        self.max_queue_size = max_queue_size
        self.packets = []
        self.processed_packets = []
        self.dropped_packets = []  # Track dropped packets
        self.current_time = 0.0
    
    def add_packet(self, packet):
        """Add a packet to the queue."""
        raise NotImplementedError
    
    def process_next(self):
        """Process the next packet in the queue."""
        raise NotImplementedError
    
    def is_empty(self):
        """Check if queue is empty."""
        raise NotImplementedError
    
    def get_queue_size(self):
        """Get current queue size."""
        raise NotImplementedError
    
    def get_metrics(self):
        """
        Calculate performance metrics including both per-packet and per-flow fairness.
        
        Returns:
            Dictionary with latency, throughput, and fairness metrics
        """
        if not self.processed_packets:
            return {
                'avg_latency': 0,
                'avg_waiting_time': 0,
                'throughput': 0,
                'total_packets': 0,
                'fairness_index': 0,
                'flow_fairness_index': 0
            }
        
        latencies = [p.get_latency() for p in self.processed_packets if p.get_latency() is not None]
        waiting_times = [p.get_waiting_time() for p in self.processed_packets if p.get_waiting_time() is not None]
        
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        avg_waiting_time = sum(waiting_times) / len(waiting_times) if waiting_times else 0
        
        # Throughput: packets processed per unit time
        if self.current_time > 0:
            throughput = len(self.processed_packets) / self.current_time
        else:
            throughput = 0
        
        # Per-Packet Fairness: Jain's index on individual packet latencies
        if len(latencies) > 1:
            sum_sq = sum(lat ** 2 for lat in latencies)
            fairness_index = (sum(latencies) ** 2) / (len(latencies) * sum_sq) if sum_sq > 0 else 0
        else:
            fairness_index = 1.0
        
        # Per-Flow Fairness: Jain's index on average latency per flow
        # Group packets by flow (using priority as flow identifier)
        flow_latencies = {}
        for p in self.processed_packets:
            flow_id = p.priority  # Use priority as flow identifier
            if flow_id not in flow_latencies:
                flow_latencies[flow_id] = []
            if p.get_latency() is not None:
                flow_latencies[flow_id].append(p.get_latency())
        
        # Calculate average latency per flow
        avg_flow_latencies = []
        for flow_id, lats in flow_latencies.items():
            if lats:
                avg_flow_latencies.append(sum(lats) / len(lats))
        
        # Calculate Jain's fairness index on flow averages
        if len(avg_flow_latencies) > 1:
            sum_flow = sum(avg_flow_latencies)
            sum_sq_flow = sum(lat ** 2 for lat in avg_flow_latencies)
            flow_fairness_index = (sum_flow ** 2) / (len(avg_flow_latencies) * sum_sq_flow) if sum_sq_flow > 0 else 0
        else:
            flow_fairness_index = 1.0
        
        # Calculate drop rate
        total_offered = len(self.processed_packets) + len(self.dropped_packets)
        drop_rate = len(self.dropped_packets) / total_offered if total_offered > 0 else 0
        
        return {
            'avg_latency': avg_latency,
            'avg_waiting_time': avg_waiting_time,
            'throughput': throughput,
            'total_packets': len(self.processed_packets),
            'dropped_packets': len(self.dropped_packets),
            'drop_rate': drop_rate,
            'fairness_index': fairness_index,  # Per-packet fairness
            'flow_fairness_index': flow_fairness_index  # Per-flow fairness
        }


class FCFSQueue(QueueingStrategy):
    """First-Come, First-Served queuing strategy."""
    
    def __init__(self, max_queue_size=None):
        super().__init__("FCFS", max_queue_size)
        self.queue = deque()
    
    def add_packet(self, packet):
        """Add packet to FCFS queue, drop if full."""
        if self.max_queue_size is not None and len(self.queue) >= self.max_queue_size:
            # Queue is full, drop the packet
            self.dropped_packets.append(packet)
        else:
            self.queue.append(packet)
    
    def process_next(self):
        """Process next packet in arrival order."""
        if not self.queue:
            return None
        
        packet = self.queue.popleft()
        packet.set_start_time(self.current_time)
        self.current_time += packet.service_time
        packet.set_finish_time(self.current_time)
        self.processed_packets.append(packet)
        return packet
    
    def is_empty(self):
        """Check if FCFS queue is empty."""
        return len(self.queue) == 0
    
    def get_queue_size(self):
        """Get current queue size."""
        return len(self.queue)


class PriorityQueue(QueueingStrategy):
    """Priority Queuing strategy using a min-heap."""
    
    def __init__(self):
        super().__init__("Priority Queue")
        self.heap = []
    
    def add_packet(self, packet):
        """Add packet to priority queue."""
        heapq.heappush(self.heap, packet)
    
    def process_next(self):
        """Process highest priority packet."""
        if not self.heap:
            return None
        
        packet = heapq.heappop(self.heap)
        packet.set_start_time(self.current_time)
        self.current_time += packet.service_time
        packet.set_finish_time(self.current_time)
        self.processed_packets.append(packet)
        return packet
    
    def is_empty(self):
        """Check if priority queue is empty."""
        return len(self.heap) == 0


class RoundRobinQueue(QueueingStrategy):
    """Round-Robin queuing strategy with multiple queues."""
    
    def __init__(self, num_queues=3, time_quantum=0.5):
        """
        Initialize Round-Robin queue.
        
        Args:
            num_queues: Number of separate queues
            time_quantum: Time slice for each queue
        """
        super().__init__("Round-Robin")
        self.num_queues = num_queues
        self.time_quantum = time_quantum
        self.queues = [deque() for _ in range(num_queues)]
        self.current_queue_index = 0
    
    def add_packet(self, packet):
        """
        Add packet to a queue based on its properties.
        We'll use packet ID modulo to distribute packets across queues.
        """
        queue_idx = packet.id % self.num_queues
        self.queues[queue_idx].append(packet)
    
    def process_next(self):
        """Process next packet using Round-Robin scheduling."""
        # Find next non-empty queue
        attempts = 0
        while attempts < self.num_queues:
            if self.queues[self.current_queue_index]:
                break
            self.current_queue_index = (self.current_queue_index + 1) % self.num_queues
            attempts += 1
        
        # All queues empty
        if attempts >= self.num_queues:
            return None
        
        # Get packet from current queue
        packet = self.queues[self.current_queue_index].popleft()
        
        # Process packet (use full service time or time quantum, whichever is smaller)
        if packet.start_time is None:
            packet.set_start_time(self.current_time)
        
        # For simplicity, we process entire packet (not preemptive)
        self.current_time += packet.service_time
        packet.set_finish_time(self.current_time)
        self.processed_packets.append(packet)
        
        # Move to next queue for Round-Robin
        self.current_queue_index = (self.current_queue_index + 1) % self.num_queues
        
        return packet
    
    def is_empty(self):
        """Check if all queues are empty."""
        return all(len(q) == 0 for q in self.queues)


class FairQueue(QueueingStrategy):
    """
    Fair Queueing (FQ) strategy.
    
    Maintains separate queues for different flows and uses virtual finish times
    to approximate bit-by-bit round-robin scheduling. This ensures fairness
    across flows regardless of packet sizes or arrival patterns.
    """
    
    def __init__(self, max_queue_size=None):
        """Initialize Fair Queue."""
        super().__init__("Fair Queue", max_queue_size)
        self.flow_queues = {}  # Dictionary: flow_id -> deque of packets
        self.virtual_time = 0.0  # Virtual time for fairness calculation
        self.flow_finish_times = {}  # Dictionary: flow_id -> virtual finish time
    
    def _get_flow_id(self, packet):
        """
        Determine flow ID for a packet.
        In this simulation, we use priority as flow identifier.
        In real networks, this would be based on source/dest IP and ports.
        
        Args:
            packet: Packet to classify
            
        Returns:
            Flow identifier
        """
        return packet.priority
    
    def add_packet(self, packet):
        """
        Add packet to its flow queue with per-flow fair dropping.
        
        Fair Queue uses per-flow queue limits to ensure fair dropping:
        - Each flow gets equal share of buffer space
        - Protects small flows from aggressive large flows
        
        Args:
            packet: Packet to add
        """
        flow_id = self._get_flow_id(packet)
        
        # Create new flow queue if needed
        if flow_id not in self.flow_queues:
            self.flow_queues[flow_id] = deque()
            self.flow_finish_times[flow_id] = 0.0
        
        # Fair dropping: check per-flow limit
        if self.max_queue_size is not None:
            # Calculate fair share per flow
            num_flows = len(self.flow_queues)
            per_flow_limit = max(1, self.max_queue_size // num_flows)
            
            # Check if this flow exceeds its fair share
            if len(self.flow_queues[flow_id]) >= per_flow_limit:
                # This flow has used its fair share, drop the packet
                self.dropped_packets.append(packet)
                return
        
        self.flow_queues[flow_id].append(packet)
    
    def process_next(self):
        """
        Process next packet using Fair Queueing algorithm.
        
        Uses round-robin across flows to ensure each flow gets equal service,
        providing max-min fairness.
        
        Returns:
            Processed packet or None if all queues empty
        """
        if not self.flow_queues:
            return None
        
        # Remove empty flow queues
        empty_flows = [fid for fid, q in self.flow_queues.items() if len(q) == 0]
        for fid in empty_flows:
            del self.flow_queues[fid]
            if fid in self.flow_finish_times:
                del self.flow_finish_times[fid]
        
        if not self.flow_queues:
            return None
        
        # Simple round-robin: serve flows in order of their finish times
        # Flow with smallest finish time gets to send next
        min_flow_id = min(self.flow_queues.keys(), 
                         key=lambda fid: (self.flow_finish_times[fid], fid))
        
        # Dequeue packet from selected flow
        packet = self.flow_queues[min_flow_id].popleft()
        
        # Update this flow's virtual finish time
        # Each flow accumulates service time independently
        self.flow_finish_times[min_flow_id] += packet.service_time
        
        # Global virtual time tracks the minimum (ensures fairness)
        if self.flow_finish_times:
            self.virtual_time = min(self.flow_finish_times.values())
        
        # Process packet in real time
        packet.set_start_time(self.current_time)
        self.current_time += packet.service_time
        packet.set_finish_time(self.current_time)
        self.processed_packets.append(packet)
        
        return packet
    
    def is_empty(self):
        """
        Check if all flow queues are empty.
        
        Returns:
            True if no packets in any flow queue
        """
        return all(len(q) == 0 for q in self.flow_queues.values()) if self.flow_queues else True
    
    def get_queue_size(self):
        """Get total queue size across all flows."""
        return sum(len(q) for q in self.flow_queues.values())
