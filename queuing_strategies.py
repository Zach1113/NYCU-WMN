"""
Queuing strategies for Quality of Service (QoS) simulation.
"""

import heapq
from collections import deque
from packet import Packet


class QueueingStrategy:
    """Base class for queuing strategies."""
    
    def __init__(self, name):
        """
        Initialize the queuing strategy.
        
        Args:
            name: Name of the strategy
        """
        self.name = name
        self.packets = []
        self.processed_packets = []
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
    
    def get_metrics(self):
        """
        Calculate performance metrics.
        
        Returns:
            Dictionary with latency, throughput, and fairness metrics
        """
        if not self.processed_packets:
            return {
                'avg_latency': 0,
                'avg_waiting_time': 0,
                'throughput': 0,
                'total_packets': 0,
                'fairness_index': 0
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
        
        # Fairness: calculate variance in latencies (lower variance = more fair)
        if len(latencies) > 1:
            mean_lat = avg_latency
            variance = sum((lat - mean_lat) ** 2 for lat in latencies) / len(latencies)
            # Jain's fairness index
            sum_sq = sum(lat ** 2 for lat in latencies)
            fairness_index = (sum(latencies) ** 2) / (len(latencies) * sum_sq) if sum_sq > 0 else 0
        else:
            fairness_index = 1.0
        
        return {
            'avg_latency': avg_latency,
            'avg_waiting_time': avg_waiting_time,
            'throughput': throughput,
            'total_packets': len(self.processed_packets),
            'fairness_index': fairness_index
        }


class FCFSQueue(QueueingStrategy):
    """First-Come, First-Served queuing strategy."""
    
    def __init__(self):
        super().__init__("FCFS")
        self.queue = deque()
    
    def add_packet(self, packet):
        """Add packet to FCFS queue."""
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
    
    def __init__(self):
        """Initialize Fair Queue."""
        super().__init__("Fair Queue")
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
        Add packet to its flow queue.
        
        Args:
            packet: Packet to add
        """
        flow_id = self._get_flow_id(packet)
        
        # Create new flow queue if needed
        if flow_id not in self.flow_queues:
            self.flow_queues[flow_id] = deque()
            self.flow_finish_times[flow_id] = 0.0
        
        self.flow_queues[flow_id].append(packet)
    
    def process_next(self):
        """
        Process next packet using Fair Queueing algorithm.
        
        Selects the packet with the smallest virtual finish time,
        which approximates bit-by-bit round-robin fairness.
        
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
        
        # Find flow with minimum virtual finish time
        min_flow_id = None
        min_finish_time = float('inf')
        
        for flow_id, queue in self.flow_queues.items():
            if len(queue) > 0:
                # Calculate virtual finish time for the head packet
                packet = queue[0]
                
                # Virtual start time is max of current virtual time and flow's last finish time
                virtual_start = max(self.virtual_time, self.flow_finish_times[flow_id])
                
                # Virtual finish time = virtual start + packet size / link capacity
                # We use service_time as a proxy for packet size / capacity
                virtual_finish = virtual_start + packet.service_time
                
                if virtual_finish < min_finish_time:
                    min_finish_time = virtual_finish
                    min_flow_id = flow_id
        
        if min_flow_id is None:
            return None
        
        # Dequeue packet from selected flow
        packet = self.flow_queues[min_flow_id].popleft()
        
        # Update virtual time to the finish time of the packet being processed
        virtual_start = max(self.virtual_time, self.flow_finish_times[min_flow_id])
        virtual_finish = virtual_start + packet.service_time
        
        self.virtual_time = virtual_finish
        self.flow_finish_times[min_flow_id] = virtual_finish
        
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
